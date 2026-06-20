import pandas as pd
from datetime import timedelta
import json
import argparse
import sys
import os

class LagEvaluator:
    """
    Evaluates lag time between detected signals and official incidents.
    Lag > 0 means the signal preceded the incident (early warning).
    """
    def __init__(self, max_lag_days=7):
        # Maximum days to look forward for an incident after a signal
        self.max_lag_days = max_lag_days

    def evaluate(self, signals_df: pd.DataFrame, incidents_df: pd.DataFrame, region="Jawa") -> dict:
        """
        Compare signals against incidents and calculate metrics.
        Returns a dictionary of metrics and a dataframe of detailed matches.
        """
        # Ensure datetime format
        signals = signals_df.copy()
        signals['window_date'] = pd.to_datetime(signals['window_date'])
        
        incidents = incidents_df.copy()
        incidents['date'] = pd.to_datetime(incidents['date'])
        
        # Filter for signals (is_signal == True) and specific region
        signals = signals[(signals['is_signal'] == True) & (signals['region'] == region)].sort_values('window_date')
        incidents = incidents[incidents['region'].isin(['Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'DKI Jakarta', 'DI Yogyakarta', 'Banten'])].sort_values('date')
        
        validation_records = []
        matched_incident_indices = set()
        
        for idx, signal in signals.iterrows():
            sig_date = signal['window_date']
            
            # Find incidents in [sig_date, sig_date + max_lag_days]
            window_end = sig_date + timedelta(days=self.max_lag_days)
            
            # We look for incidents at the province level (Jawa provinces)
            # For simplicity in MVP, if region is just "Jawa", we check all Jawa provinces
            potential_matches = incidents[
                (incidents['date'] >= sig_date) & 
                (incidents['date'] <= window_end)
            ]
            
            if len(potential_matches) > 0:
                # Take the earliest matching incident in the window
                best_match = potential_matches.iloc[0]
                incident_idx = potential_matches.index[0]
                
                lag_days = (best_match['date'] - sig_date).days
                
                validation_records.append({
                    "signal_id": signal.get('id', f"sig_{sig_date.strftime('%Y%m%d')}"),
                    "signal_date": sig_date,
                    "matched_incident_id": f"inc_{best_match['date'].strftime('%Y%m%d')}_{incident_idx}",
                    "lag_days": int(lag_days),
                    "matched": True,
                    "incident_date": best_match['date'],
                    "incident_location": best_match['location'],
                    "incident_victim_count": int(best_match['victim_count']),
                    "region": region
                })
                matched_incident_indices.add(incident_idx)
            else:
                # No match found within window (False Positive)
                validation_records.append({
                    "signal_id": signal.get('id', f"sig_{sig_date.strftime('%Y%m%d')}"),
                    "signal_date": sig_date,
                    "matched_incident_id": None,
                    "lag_days": None,
                    "matched": False,
                    "incident_date": None,
                    "incident_location": None,
                    "incident_victim_count": None,
                    "region": region
                })
                
        val_df = pd.DataFrame(validation_records)
        
        # Calculate metrics
        total_signals = len(signals)
        total_incidents = len(incidents)
        matched_incidents = len(matched_incident_indices)
        
        match_rate_pct = (matched_incidents / total_incidents * 100) if total_incidents > 0 else 0
        
        if len(val_df) > 0 and val_df['matched'].sum() > 0:
            avg_lag = val_df[val_df['matched'] == True]['lag_days'].mean()
            median_lag = val_df[val_df['matched'] == True]['lag_days'].median()
        else:
            avg_lag = None
            median_lag = None
            
        metrics = {
            "total_signals_detected": int(total_signals),
            "total_incidents_recorded": int(total_incidents),
            "matched_incidents": int(matched_incidents),
            "match_rate_pct": float(round(match_rate_pct, 2)),
            "avg_lag_days": float(round(avg_lag, 2)) if avg_lag is not None else None,
            "median_lag_days": float(round(median_lag, 2)) if median_lag is not None else None
        }
        
        return metrics, val_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate lag time between signals and incidents")
    parser.add_argument("--signals", type=str, help="Path to signals CSV", default="test_signals.csv")
    parser.add_argument("--incidents", type=str, help="Path to incidents CSV", default="../../incidents_wilayah_ii.csv")
    parser.add_argument("--test", action="store_true", help="Run with dummy test data")
    args = parser.parse_args()
    
    evaluator = LagEvaluator(max_lag_days=7)
    
    if args.test:
        print("Running Lag Evaluator with test data...")
        
        # Create dummy signals
        signals_data = {
            'id': ['sig_1', 'sig_2', 'sig_3'],
            'window_date': ['2025-04-18', '2025-08-10', '2025-12-01'],
            'region': ['Jawa', 'Jawa', 'Jawa'],
            'is_signal': [True, True, True]
        }
        sig_df = pd.DataFrame(signals_data)
        
        # Create dummy incidents
        incidents_data = {
            'date': ['2025-04-21', '2025-08-11', '2025-10-01'], # Match (lag=3), Match (lag=1), No Match
            'location': ['Cianjur', 'Sragen', 'Banjar'],
            'region': ['Jawa Barat', 'Jawa Tengah', 'Jawa Barat'],
            'victim_count': [176, 251, 79]
        }
        inc_df = pd.DataFrame(incidents_data)
        
        metrics, details = evaluator.evaluate(sig_df, inc_df)
        
        print("\nMetrics:")
        print(json.dumps(metrics, indent=2))
        print("\nDetails:")
        print(details[['signal_date', 'matched', 'lag_days', 'incident_location']])
    else:
        # Resolve path relative to script location if it's incidents_wilayah_ii.csv
        script_dir = os.path.dirname(os.path.abspath(__file__))
        incidents_path = args.incidents
        if "incidents_wilayah_ii.csv" in incidents_path:
            # Point to root folder where it was generated
            incidents_path = os.path.join(script_dir, "../../incidents_wilayah_ii.csv")
            
        if not os.path.exists(incidents_path):
            print(f"Error: Incidents file not found at {incidents_path}")
            sys.exit(1)
            
        if not os.path.exists(args.signals):
            print(f"Error: Signals file not found at {args.signals}")
            print("Run with --test to use dummy data instead.")
            sys.exit(1)
            
        sig_df = pd.read_csv(args.signals)
        inc_df = pd.read_csv(incidents_path)
        
        metrics, details = evaluator.evaluate(sig_df, inc_df)
        print(json.dumps(metrics, indent=2))
