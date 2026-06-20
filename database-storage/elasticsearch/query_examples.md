# Elasticsearch Query Examples — NutriWatch Dashboard

Contoh query REST API untuk kedua index utama, digunakan oleh dashboard React.

---

## 1. Signal Events

### Get all signals in last 30 days

```bash
GET /signal_events/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "window_date": {
              "gte": "now-30d/d",
              "lte": "now/d"
            }
          }
        }
      ]
    }
  },
  "sort": [
    { "window_date": "desc" }
  ],
  "size": 100
}
```

### Get only anomaly signals (is_signal = true)

```bash
GET /signal_events/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "is_signal": true } },
        {
          "range": {
            "window_date": {
              "gte": "now-30d/d"
            }
          }
        }
      ]
    }
  },
  "sort": [
    { "anomaly_score": "desc" }
  ]
}
```

### Get signals by region

```bash
GET /signal_events/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "region": "Jawa" } },
        { "term": { "is_signal": true } }
      ]
    }
  }
}
```

### Aggregate: daily tweet volume trend

```bash
GET /signal_events/_search
{
  "size": 0,
  "aggs": {
    "daily_volume": {
      "date_histogram": {
        "field": "window_date",
        "calendar_interval": "day"
      },
      "aggs": {
        "avg_volume": { "avg": { "field": "tweet_volume" } },
        "avg_negative": { "avg": { "field": "negative_ratio" } }
      }
    }
  }
}
```

### Aggregate: dominant aspect distribution

```bash
GET /signal_events/_search
{
  "size": 0,
  "query": {
    "range": {
      "window_date": { "gte": "now-30d/d" }
    }
  },
  "aggs": {
    "aspect_counts": {
      "terms": {
        "field": "dominant_aspect",
        "size": 4
      }
    }
  }
}
```

---

## 2. Validation Results

### Get all validation results

```bash
GET /validation_results/_search
{
  "query": { "match_all": {} },
  "sort": [
    { "signal_date": "desc" }
  ],
  "size": 200
}
```

### Get matched validations only

```bash
GET /validation_results/_search
{
  "query": {
    "term": { "matched": true }
  },
  "sort": [
    { "lag_days": "asc" }
  ]
}
```

### Aggregate: match rate statistics

```bash
GET /validation_results/_search
{
  "size": 0,
  "aggs": {
    "match_stats": {
      "terms": {
        "field": "matched"
      }
    },
    "lag_stats": {
      "filter": { "term": { "matched": true } },
      "aggs": {
        "avg_lag": { "avg": { "field": "lag_days" } },
        "median_lag": {
          "percentiles": {
            "field": "lag_days",
            "percents": [50]
          }
        }
      }
    }
  }
}
```

### Get validations by region

```bash
GET /validation_results/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "region": "Jawa" } },
        { "term": { "matched": true } }
      ]
    }
  }
}
```

---

## 3. Dashboard Endpoint Mapping

| Dashboard Endpoint | ES Index | Query Type |
|---|---|---|
| `GET /api/signals?days=30` | `signal_events` | Range filter on `window_date` |
| `GET /api/aspects?days=30` | `signal_events` | Aggregation on `dominant_aspect` |
| `GET /api/incidents?days=30` | N/A (from HDFS/CSV) | Direct CSV read |
| `GET /api/validation?days=30` | `validation_results` | Range filter on `signal_date` |
| `GET /api/stats` | Both indices | Aggregation queries |
| `GET /api/pipeline-status` | N/A | Live Kafka/Spark metrics |
