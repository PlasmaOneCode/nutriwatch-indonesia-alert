# Database & Storage Layer

Lapisan ini menyediakan dua jenis storage untuk ekosistem NutriWatch:

| Komponen | Peran | Tipe Data |
|---|---|---|
| **HDFS** | Cold storage | Raw events (landing zone dari Kafka/NiFi) & dataset training model ML/NLP |
| **Elasticsearch** | Hot index | Data yang dibaca dashboard React (alerts, sentiment ABSA, risk zones, stats) |

---

## 1. Struktur Folder

```text
database-storage/
├── docker-compose.yml              # HDFS (NameNode + 2 DataNode), Elasticsearch, Kibana
├── hdfs/
│   └── config/
│       └── hadoop.env              # core-site & hdfs-site (replication factor = 2)
├── elasticsearch/
│   ├── mappings/
│   │   ├── nutriwatch-alerts.json       # -> AlertPanel.tsx
│   │   ├── nutriwatch-sentiment.json    # -> SentimentGrid.tsx
│   │   ├── nutriwatch-risk-zones.json   # -> RiskMap.tsx
│   │   └── nutriwatch-stats.json        # -> StatStrip.tsx
│   └── ilm/
│       └── nutriwatch-alerts-ilm-policy.json   # retensi 90 hari, rollover harian
└── scripts/
    ├── setup_hdfs_dirs.sh           # buat struktur direktori HDFS
    ├── setup_elasticsearch_indices.sh  # apply ILM policy + buat index & mapping
    ├── index_seed_data.py           # isi data dummy untuk testing dashboard
    ├── seed_data.json               # data dummy (selaras dengan komponen frontend)
    └── verify_cluster.sh            # cek kesehatan cluster & latensi query
```

---

## 2. Cara Menjalankan

### a. Jalankan cluster

```bash
cd database-storage
docker compose up -d
```

Tunggu hingga semua container `healthy`:
- NameNode UI: http://localhost:9870
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

### b. Setup struktur direktori HDFS

```bash
bash scripts/setup_hdfs_dirs.sh
```

Membuat zona berikut di HDFS:

```text
/nutriwatch/landing/{dapur-umum-events, keluhan-stream, anggaran-events}
/nutriwatch/processed/{alerts, sentiment_absa, risk_zones}
/nutriwatch/datasets/{indobert_absa, isolation_forest}
```

### c. Setup index & mapping Elasticsearch

```bash
bash scripts/setup_elasticsearch_indices.sh
```

Membuat:
- ILM policy `nutriwatch-alerts-ilm-policy` (rollover harian, retensi 90 hari)
- Index `nutriwatch-alerts-000001` (alias write: `nutriwatch-alerts`)
- Index `nutriwatch-sentiment`, `nutriwatch-risk-zones`, `nutriwatch-stats`

### d. (Opsional) Isi data dummy untuk pengujian dashboard

```bash
pip install --user requests   # tidak wajib, skrip hanya pakai urllib bawaan
python3 scripts/index_seed_data.py
```

### e. Verifikasi cluster

```bash
bash scripts/verify_cluster.sh
```

---

## 3. Skema Index Elasticsearch (Ringkasan)

| Index | Dipakai oleh | Field kunci |
|---|---|---|
| `nutriwatch-alerts` | `AlertPanel.tsx` | `level`, `title`, `message`, `location` (geo_point), `created_at` |
| `nutriwatch-sentiment` | `SentimentGrid.tsx` | `aspect`, `positive_score`, `delta_pct` |
| `nutriwatch-risk-zones` | `RiskMap.tsx` | `zone_id`, `location` (geo_point), `risk_level`, `risk_score` |
| `nutriwatch-stats` | `StatStrip.tsx` | `metric_key`, `label`, `value`, `unit` |

Semua index `nutriwatch-*` dirancang agar query dashboard (filter, sort by waktu,
geo bounding box untuk peta) tetap di bawah 200ms pada skala data lab.

---
