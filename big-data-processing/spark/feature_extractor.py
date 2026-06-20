import pandas as pd
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ml-nlp')))
from anomaly.isolation_forest import SignalDetector

def extract_features(raw_data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a dataframe of raw processed texts (with aspect and sentiment),
    aggregate them into daily window features per region.
    """
    if raw_data_df.empty:
        return pd.DataFrame()
        
    # Ensure datetime
    raw_data_df['timestamp'] = pd.to_datetime(raw_data_df['timestamp'])
    
    # Extract date for windowing (1 day windows)
    raw_data_df['window_date'] = raw_data_df['timestamp'].dt.date
    
    # Group by date and region
    grouped = raw_data_df.groupby(['window_date', 'region'])
    
    features = []
    
    for (date, region), group in grouped:
        tweet_volume = len(group)
        
        # Calculate negative ratio
        negatives = group[group['sentiment'] == 'negative']
        negative_ratio = (len(negatives) / tweet_volume * 100) if tweet_volume > 0 else 0
        
        # Calculate dominant aspect (only among negative complaints)
        if len(negatives) > 0:
            dominant_aspect = negatives['aspect'].mode().iloc[0]
        else:
            # If no negatives, look at all aspects, or default
            if len(group) > 0 and group['aspect'].nunique() > 0:
                # filter out 'none' or 'error' if possible
                valid_aspects = group[~group['aspect'].isin(['none', 'error'])]
                if len(valid_aspects) > 0:
                    dominant_aspect = valid_aspects['aspect'].mode().iloc[0]
                else:
                    dominant_aspect = "none"
            else:
                dominant_aspect = "none"
                
        features.append({
            'window_date': date,
            'region': region,
            'tweet_volume': int(tweet_volume),
            'negative_ratio': float(round(negative_ratio, 2)),
            'dominant_aspect': str(dominant_aspect)
        })
        
    features_df = pd.DataFrame(features)
    return features_df

def process_and_detect_anomalies(features_df: pd.DataFrame, model_path="model.pkl"):
    """Run isolation forest to detect signals on the feature windows."""
    detector = SignalDetector(contamination=0.1, model_path=model_path)
    
    # In a real streaming environment, we'd load a pre-trained model
    # For MVP testing, if model doesn't exist, we fit it on the batch
    if not os.path.exists(model_path):
        print("Training initial anomaly detection model...")
        detector.fit(features_df)
        
    results = detector.predict(features_df)
    return results

if __name__ == "__main__":
    print("Testing Feature Extractor...")
    # Create dummy raw data
    dummy_data = pd.DataFrame({
        'timestamp': pd.date_range(start='2025-09-01', periods=10, freq='4h'),
        'region': ['Jawa'] * 10,
        'sentiment': ['negative', 'positive', 'negative', 'negative', 'neutral', 
                      'negative', 'negative', 'positive', 'negative', 'negative'],
        'aspect': ['porsi_kecukupan', 'rasa_menu', 'porsi_kecukupan', 'higienitas_keamanan', 'rasa_menu',
                   'higienitas_keamanan', 'higienitas_keamanan', 'rasa_menu', 'porsi_kecukupan', 'higienitas_keamanan']
    })
    
    print("\nRaw Data (first 5 rows):")
    print(dummy_data.head())
    
    features = extract_features(dummy_data)
    print("\nExtracted Features:")
    print(features)
    
    print("\nAnomaly Detection:")
    results = process_and_detect_anomalies(features, model_path="test_model.pkl")
    print(results)
    
    if os.path.exists("test_model.pkl"):
        os.remove("test_model.pkl")
