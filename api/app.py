from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Mock Data / Elasticsearch Interface
# In production, this would query Elasticsearch indices:
# 'signal_events' and 'validation_results'

def generate_mock_signals(days=30):
    signals = []
    base_date = datetime.now() - timedelta(days=days)
    aspects = ["rasa_menu", "porsi_kecukupan", "distribusi_ketepatan", "higienitas_keamanan"]
    
    for i in range(15):  # 15 random signals
        sig_date = base_date + timedelta(days=random.randint(0, days))
        signals.append({
            "id": f"sig_{i}",
            "window_date": sig_date.strftime("%Y-%m-%d"),
            "region": "Jawa",
            "anomaly_score": round(random.uniform(0.6, 0.99), 2),
            "is_signal": True,
            "tweet_volume": random.randint(100, 500),
            "negative_ratio": round(random.uniform(40, 90), 1),
            "dominant_aspect": random.choice(aspects)
        })
    return sorted(signals, key=lambda x: x["window_date"], reverse=True)

@app.route('/api/signals', methods=['GET'])
def get_signals():
    days = int(request.args.get('days', 30))
    # TODO: Query ES `signal_events` index
    # GET /signal_events/_search where window_date >= now-days
    
    return jsonify(generate_mock_signals(days))

@app.route('/api/aspects', methods=['GET'])
def get_aspects():
    days = int(request.args.get('days', 30))
    # TODO: Query ES `signal_events` index with aggregations
    
    base_date = datetime.now().strftime("%Y-%m-%d")
    return jsonify([
        {
            "aspect": "higienitas_keamanan",
            "negative_pct": 85.5,
            "total_mentions": 1420,
            "window_date": base_date
        },
        {
            "aspect": "porsi_kecukupan",
            "negative_pct": 62.0,
            "total_mentions": 850,
            "window_date": base_date
        },
        {
            "aspect": "rasa_menu",
            "negative_pct": 45.0,
            "total_mentions": 600,
            "window_date": base_date
        },
        {
            "aspect": "distribusi_ketepatan",
            "negative_pct": 30.5,
            "total_mentions": 320,
            "window_date": base_date
        }
    ])

@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    days = int(request.args.get('days', 30))
    # TODO: Read from HDFS or query local incidents CSV
    
    return jsonify([
        {
            "id": "inc_1",
            "date": "2025-04-21",
            "sppg_name": "SPPG Cianjur",
            "location": "MAN 1 dan SMP PGRI 1 Cianjur",
            "region": "Jawa Barat",
            "victim_count": 176,
            "source": "Tempo"
        },
        {
            "id": "inc_2",
            "date": "2025-09-16",
            "sppg_name": "SPPG Al Bayyinah",
            "location": "Kadungora Garut",
            "region": "Jawa Barat",
            "victim_count": 657,
            "source": "Tempo"
        }
    ])

@app.route('/api/validation', methods=['GET'])
def get_validation():
    days = int(request.args.get('days', 30))
    # TODO: Query ES `validation_results` index
    
    return jsonify([
        {
            "signal_id": "sig_1",
            "matched_incident_id": "inc_1",
            "lag_days": 3,
            "matched": True
        },
        {
            "signal_id": "sig_2",
            "matched_incident_id": None,
            "lag_days": None,
            "matched": False
        }
    ])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    # TODO: Perform aggregate queries on both indices
    
    return jsonify({
        "region": "Jawa",
        "total_texts_processed": 45800,
        "total_signals_detected": 15,
        "total_incidents_recorded": 196,
        "match_rate_pct": 75.5,
        "avg_lag_days": 2.4,
        "median_lag_days": 2.0,
        "last_updated": datetime.now().isoformat()
    })

@app.route('/api/pipeline-status', methods=['GET'])
def get_pipeline_status():
    # TODO: Fetch live metrics from Kafka JMX and Spark REST API
    
    return jsonify({
        "kafka_topics": [
            { "name": "mbg-text-stream", "msg_per_min": 120, "lag": 5 }
        ],
        "spark_throughput_rps": 2.5,
        "model_versions": [
            { "name": "IndoBERT-ABSA", "version": "zero-shot-mDeBERTa" },
            { "name": "IsolationForest", "version": "v1.0-contamination-0.1" }
        ],
        "stream_healthy": True
    })

if __name__ == '__main__':
    # Run on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
