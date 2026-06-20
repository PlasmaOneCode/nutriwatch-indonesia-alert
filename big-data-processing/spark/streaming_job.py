from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, udf, count, avg, max as spark_max
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, MapType
import sys
import os

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

print("Setting up ABSA Model...")
absa_model = IndoBERTAbsaZeroShot(device=-1) # CPU for Spark execution safety, or adjust based on resources

def predict_absa(text):
    if not text:
        return {"aspect": "none", "sentiment": "neutral", "confidence": 0.0}
    try:
        return absa_model.predict(text)
    except Exception:
        return {"aspect": "error", "sentiment": "neutral", "confidence": 0.0}

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

    # Write raw output to HDFS (or local console for testing)
    # Using console for MVP testing to avoid HDFS complexity during debug
    raw_query = processed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", False) \
        .start()
        
    # Example for HDFS writing (uncomment for prod):
    # raw_query = processed_df.writeStream \
    #     .outputMode("append") \
    #     .format("json") \
    #     .option("path", "hdfs://localhost:9000/nutriwatch/raw_text/") \
    #     .option("checkpointLocation", "/tmp/spark-checkpoints-raw") \
    #     .start()

    raw_query.awaitTermination()

if __name__ == "__main__":
    main()
