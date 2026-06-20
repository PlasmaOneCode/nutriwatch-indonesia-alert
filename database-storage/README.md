# Database & Storage — NutriWatch

Modul ini mendefinisikan skema penyimpanan untuk seluruh pipeline NutriWatch.

## Komponen

### 1. HDFS (Hadoop Distributed File System)

Menyimpan data mentah dan hasil pemrosesan:

| Path | Isi | Format |
|------|-----|--------|
| `/nutriwatch/raw_text/year=.../month=.../day=.../` | Log teks mentah + hasil ABSA | JSON Lines |
| `/nutriwatch/features/daily/year=.../month=.../` | Fitur window harian | Parquet |
| `/nutriwatch/incidents/raw/` | Data insiden resmi | CSV |

Lihat file `schema_*.md` di folder `hdfs/` untuk detail kolom dan partisi.

### 2. Elasticsearch

Menyimpan data yang di-query oleh dashboard React:

| Index | Isi | Mapping File |
|-------|-----|------|
| `signal_events` | Window signals + anomaly scores | `index_signal_events.json` |
| `validation_results` | Hasil lag-time validation | `index_validation.json` |

Lihat `query_examples.md` untuk contoh query REST.

## Setup

### HDFS

HDFS berjalan di Docker via `docker-compose.yml` di root project:

```bash
# Start HDFS
docker-compose up -d namenode datanode

# Buat direktori di HDFS
docker exec nutriwatch-namenode hdfs dfs -mkdir -p /nutriwatch/raw_text
docker exec nutriwatch-namenode hdfs dfs -mkdir -p /nutriwatch/features/daily
docker exec nutriwatch-namenode hdfs dfs -mkdir -p /nutriwatch/incidents/raw

# Verifikasi
docker exec nutriwatch-namenode hdfs dfs -ls /nutriwatch/
```

Web UI: http://localhost:9870

### Elasticsearch

```bash
# Start Elasticsearch
docker-compose up -d elasticsearch

# Buat index signal_events
curl -X PUT "localhost:9200/signal_events" -H "Content-Type: application/json" -d @database-storage/elasticsearch/index_signal_events.json

# Buat index validation_results
curl -X PUT "localhost:9200/validation_results" -H "Content-Type: application/json" -d @database-storage/elasticsearch/index_validation.json

# Verifikasi
curl "localhost:9200/_cat/indices?v"
```

Web UI: http://localhost:9200
