import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import pickle
import os
import argparse

class SignalDetector:
    """
    Anomaly detection using Isolation Forest to identify 'signals'
    from daily feature windows.
    """
    def __init__(self, contamination=0.1, model_path="model.pkl"):
        self.contamination = contamination
        self.model_path = model_path
        self.model = IsolationForest(
            n_estimators=100, 
            max_samples='auto', 
            contamination=self.contamination, 
            random_state=42
        )
        self.is_fitted = False
        
        # Features used for training
        self.feature_cols = [
            'tweet_volume', 
            'negative_ratio',
            'aspect_rasa_menu',
            'aspect_porsi_kecukupan',
            'aspect_distribusi_ketepatan',
            'aspect_higienitas_keamanan'
        ]

    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """One-hot encode dominant_aspect and ensure all columns exist."""
        # Create a copy
        processed = df.copy()
        
        # One-hot encode dominant_aspect
        if 'dominant_aspect' in processed.columns:
            dummies = pd.get_dummies(processed['dominant_aspect'], prefix='aspect')
            processed = pd.concat([processed, dummies], axis=1)
            
        # Ensure all required features exist (fill missing with 0)
        for col in self.feature_cols:
            if col not in processed.columns:
                processed[col] = 0
                
        # Fill NaNs
        processed = processed.fillna(0)
        
        return processed[self.feature_cols]

    def fit(self, df: pd.DataFrame):
        """Train the Isolation Forest model on historical data."""
        X = self._preprocess(df)
        self.model.fit(X)
        self.is_fitted = True
        
        # Save model
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
            
        print(f"Model trained and saved to {self.model_path}")
        return self

    def load_model(self):
        """Load trained model from disk."""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            self.is_fitted = True
            print(f"Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"Model file not found at {self.model_path}. Call fit() first.")

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict anomalies for the given windows.
        Returns original dataframe with 'anomaly_score' and 'is_signal' added.
        """
        if not self.is_fitted:
            self.load_model()
            
        X = self._preprocess(df)
        
        # Predict: 1 for inliers, -1 for outliers/anomalies
        preds = self.model.predict(X)
        
        # Score_samples returns negative anomaly scores. 
        # Lower = more anomalous. We invert and normalize it to 0-1 range roughly
        # For sklearn IsolationForest, decision_function is usually < 0 for anomalies
        scores = self.model.decision_function(X)
        
        # Normalize score to 0-1 where 1 is highest anomaly (most negative original score)
        # We use a simple normalization based on min/max of the batch for simplicity
        # In production, we'd use robust scaler based on training data
        if len(scores) > 1 and scores.max() != scores.min():
            norm_scores = (scores.max() - scores) / (scores.max() - scores.min())
        else:
            norm_scores = np.where(preds == -1, 0.8, 0.2)
            
        result = df.copy()
        result['anomaly_score'] = norm_scores
        result['is_signal'] = (preds == -1)
        
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Isolation Forest Anomaly Detection")
    parser.add_argument("--test", action="store_true", help="Run tests")
    args = parser.parse_args()
    
    if args.test:
        print("\nTesting Isolation Forest Anomaly Detector")
        print("-" * 50)
        
        # Generate dummy historical data (normal)
        # ~100 tweets/day, ~20% negative, aspect mainly porsi
        np.random.seed(42)
        n_samples = 30
        
        normal_data = pd.DataFrame({
            'window_date': pd.date_range(start='2025-01-01', periods=n_samples),
            'region': ['Jawa'] * n_samples,
            'tweet_volume': np.random.normal(100, 20, n_samples).astype(int),
            'negative_ratio': np.random.normal(20, 5, n_samples),
            'dominant_aspect': np.random.choice(['porsi_kecukupan', 'rasa_menu'], n_samples)
        })
        
        # Add a couple of clear anomalies (spikes)
        anomaly1 = pd.DataFrame({
            'window_date': [pd.to_datetime('2025-01-31')],
            'region': ['Jawa'],
            'tweet_volume': [500], # huge volume spike
            'negative_ratio': [85.0], # huge negativity spike
            'dominant_aspect': ['higienitas_keamanan'] # alarming aspect
        })
        
        anomaly2 = pd.DataFrame({
            'window_date': [pd.to_datetime('2025-02-01')],
            'region': ['Jawa'],
            'tweet_volume': [300],
            'negative_ratio': [70.0],
            'dominant_aspect': ['higienitas_keamanan']
        })
        
        test_df = pd.concat([normal_data, anomaly1, anomaly2], ignore_index=True)
        
        detector = SignalDetector(contamination=0.1, model_path="test_model.pkl")
        detector.fit(test_df)
        
        results = detector.predict(test_df)
        
        print("\nSample of Normal Days:")
        print(results[~results['is_signal']][['window_date', 'tweet_volume', 'negative_ratio', 'anomaly_score']].head())
        
        print("\nDetected Anomalies (Signals):")
        print(results[results['is_signal']][['window_date', 'tweet_volume', 'negative_ratio', 'dominant_aspect', 'anomaly_score']])
        
        # Cleanup
        if os.path.exists("test_model.pkl"):
            os.remove("test_model.pkl")
