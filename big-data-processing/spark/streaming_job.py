from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, udf, count, avg, max as spark_max
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, MapType
import sys
import os

# Fix for Windows where Spark tries to find "python3" but only "python" exists
os.environ["PYSPARK_PYTHON"] = "python"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python"

# Fix for Thread Deadlocks in PySpark Workers on Windows
# Prevents HuggingFace Tokenizers (Rust) and PyTorch (OpenMP) from spawning threads
# inside the PySpark multiprocessing worker, which causes permanent freezes.
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

# Add ml-nlp to python path so we can import absa and anomaly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ml-nlp')))
from absa.indobert_absa import IndoBERTAbsaZeroShot

# Set up Spark Session
# In a real cluster we'd configure master differently
spark = SparkSession.builder \
    .appName("NutriWatchStreamingJob") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define schema for incoming Kafka message
schema = StructType([
    StructField("text_id", StringType(), True),
    StructField("text", StringType(), True),
    StructField("timestamp", StringType(), True), # Kafka producer sends ISO string
    StructField("source", StringType(), True),
    StructField("region", StringType(), True)
])

# We initialize the model lazily inside the UDF to prevent PySpark from trying
# to serialize the heavy PyTorch model and broadcasting it to workers,
# which causes "Failed to delete original file" TempFile IOExceptions on Windows.
def predict_absa(text):
    if not text:
        return {"aspect": "none", "sentiment": "neutral", "confidence": 0.0}
    try:
        # Lazy initialization inside the function attribute to avoid PySpark globals pickling issues
        if not hasattr(predict_absa, "model"):
            import sys
            import os
            # Ensure ml-nlp is in the worker's python path
            # __file__ in PySpark worker might not be defined reliably, so we use current working directory or hardcoded fallback
            # but since this is local mode, os.getcwd() usually points to the project root.
            # Let's dynamically find it based on os.getcwd()
            project_root = os.getcwd()
            ml_nlp_path = os.path.join(project_root, 'ml-nlp')
            if ml_nlp_path not in sys.path:
                sys.path.append(ml_nlp_path)
                
            from absa.indobert_absa import IndoBERTAbsaZeroShot
            predict_absa.model = IndoBERTAbsaZeroShot(device=-1)
        
        return predict_absa.model.predict(text)
    except Exception as e:
        import traceback
        err_msg = str(e).replace("\n", " ")
        return {"aspect": f"err: {err_msg}", "sentiment": "neutral", "confidence": 0.0}

absa_schema = MapType(StringType(), StringType())
predict_absa_udf = udf(lambda t: {k: str(v) for k, v in predict_absa(t).items()}, absa_schema)

def main():
    print("Starting Spark Structured Streaming Job...")
    
    # 1. Read from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "mbg-text-stream") \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", 10) \
        .load()

    # 2. Parse JSON
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")
        
    # Cast timestamp to actual timestamp type
    parsed_df = parsed_df.withColumn("timestamp", col("timestamp").cast(TimestampType()))

    # 3. Apply ABSA
    processed_df = parsed_df.withColumn("absa", predict_absa_udf(col("text")))
    processed_df = processed_df \
        .withColumn("aspect", col("absa").getItem("aspect")) \
        .withColumn("sentiment", col("absa").getItem("sentiment")) \
        .withColumn("confidence", col("absa").getItem("confidence").cast(DoubleType()))

    def write_to_es(batch_df, batch_id):
        # Convert small batch (max 10 rows) to Pandas
        pdf = batch_df.toPandas()
        if not pdf.empty:
            from elasticsearch import Elasticsearch
            import datetime
            
            es = Elasticsearch("http://localhost:9200")
            
            # Ensure index exists
            try:
                if not es.indices.exists(index="signal_events"):
                    es.indices.create(index="signal_events")
            except Exception as e:
                print(f"Failed to connect/create ES index: {e}")
                return
            
            for _, row in pdf.iterrows():
                try:
                    ts = row["timestamp"].isoformat() if row["timestamp"] else datetime.datetime.now().isoformat()
                    
                    doc = {
                        "text_id": str(row["text_id"]),
                        "text": str(row["text"]),
                        "window_date": ts,
                        "region": str(row["region"]),
                        "source": str(row["source"]),
                        "dominant_aspect": str(row["aspect"]),
                        "sentiment": str(row["sentiment"]),
                        "confidence": float(row["confidence"]),
                        # Flag as critical signal if negative and highly confident
                        "is_signal": bool(row["sentiment"] == "negative" and row["confidence"] > 0.8)
                    }
                    es.index(index="signal_events", id=str(row["text_id"]), document=doc)
                except Exception as e:
                    print(f"Error indexing row to ES: {e}")
            
            print(f"Indexed {len(pdf)} documents to Elasticsearch (batch {batch_id})")

    # Write output to Elasticsearch using foreachBatch
    raw_query = processed_df.writeStream \
        .outputMode("append") \
        .foreachBatch(write_to_es) \
        .start()

    raw_query.awaitTermination()

if __name__ == "__main__":
    main()
