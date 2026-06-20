import json
import time
import uuid
import yaml
import pandas as pd
from datetime import datetime
from kafka import KafkaProducer
from typing import Dict, Any

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_producer(config: Dict[str, Any]) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=config['kafka']['bootstrap_servers'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def find_column(df: pd.DataFrame, primary: str, fallbacks: list) -> str:
    """Find the best matching column name from dataframe."""
    if primary in df.columns:
        return primary
    for fb in fallbacks:
        if fb in df.columns:
            return fb
    return None

def main():
    print("=" * 80)
    print("NUTRIWATCH: Kafka Producer Replay")
    print("=" * 80)
    
    # Load config
    config = load_config()
    dataset_path = config['dataset']['path']
    topic = config['kafka']['topic']
    rate = config['replay']['rate']
    log_interval = config['logging']['log_interval']
    
    # Load dataset
    print(f"[1] Loading dataset from: {dataset_path}")
    try:
        df = pd.read_csv(dataset_path, encoding=config['dataset']['encoding'], sep=config['dataset']['separator'])
        print(f"    ✓ Loaded {len(df)} records")
    except FileNotFoundError:
        print(f"    ❌ Dataset not found at {dataset_path}")
        print("    Please create the 'datasets' folder and place the Kaggle CSV file there.")
        return
        
    # Find columns
    text_col = find_column(df, config['replay']['text_column'], config['replay']['text_column_fallbacks'])
    time_col = find_column(df, config['replay']['timestamp_column'], config['replay']['timestamp_column_fallbacks'])
    
    if not text_col:
        print(f"    ❌ Could not find a text column. Available columns: {list(df.columns)}")
        return
        
    print(f"    ✓ Using text column: '{text_col}'")
    print(f"    ✓ Using time column: '{time_col if time_col else 'Current Time (No time col found)'}'")
    
    # Setup Kafka Producer
    print(f"\n[2] Connecting to Kafka broker: {config['kafka']['bootstrap_servers']}")
    try:
        producer = setup_producer(config)
        print(f"    ✓ Connected successfully")
    except Exception as e:
        print(f"    ❌ Failed to connect: {str(e)}")
        print("    Ensure docker-compose up -d has been run and Kafka is ready.")
        return
        
    # Calculate delay
    delay = 1.0 / rate if rate > 0 else 0
    print(f"\n[3] Starting replay to topic '{topic}' at {rate if rate > 0 else 'MAX'} messages/sec")
    
    count = 0
    start_time = time.time()
    
    try:
        for idx, row in df.iterrows():
            text = str(row[text_col])
            
            # Skip empty text
            if text == 'nan' or not text.strip():
                continue
                
            # Get timestamp or use current
            if time_col and str(row[time_col]) != 'nan':
                timestamp = str(row[time_col])
            else:
                timestamp = datetime.now().isoformat()
                
            # Build message payload
            message = {
                "text_id": str(uuid.uuid4()),
                "text": text,
                "timestamp": timestamp,
                "source": "kaggle_dataset",
                "region": "Jawa"  # Default for MVP
            }
            
            # Send message
            producer.send(topic, value=message)
            count += 1
            
            # Logging
            if count % log_interval == 0:
                print(f"    ... published {count} messages (latest ID: {message['text_id'][:8]})")
                
            # Rate limiting
            if delay > 0:
                time.sleep(delay)
                
    except KeyboardInterrupt:
        print("\n    ⚠️ Replay interrupted by user")
    
    # Clean up
    producer.flush()
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("REPLAY SUMMARY")
    print("=" * 80)
    print(f"Total messages published: {count}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    if elapsed > 0:
        print(f"Actual rate: {count/elapsed:.2f} messages/sec")
    print("=" * 80)

if __name__ == "__main__":
    main()
