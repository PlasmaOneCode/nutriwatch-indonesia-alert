# Data Engineering Module — NutriWatch

Modul ini bertanggung jawab untuk memasukkan data (ingestion) ke dalam pipeline.
Ada dua aliran data utama:
1. **Streaming Teks (Kafka)**: Mensimulasikan data streaming media sosial.
2. **Batch Insiden (HDFS)**: Memasukkan data insiden keracunan historis untuk validasi.

## 1. Kafka Producer (Replay Dataset)

Mensimulasikan data streaming secara real-time dengan mereplay dataset Kaggle historis.

### Setup Dataset
1. Download dataset Kaggle (lihat link di root README).
2. Buat folder `datasets/` di root project.
3. Letakkan CSV dataset di dalam folder tersebut (misal: `datasets/mbg_tweets.csv`).
4. Update `config.yaml` jika path dataset atau nama kolom berbeda.

### Menjalankan Producer
Pastikan container Kafka sudah berjalan (`docker-compose up -d kafka`).

```bash
cd data-engineering/kafka
pip install -r requirements.txt # (kafka-python-ng, pandas, pyyaml)
python producer.py
```

## 2. Ingest Insiden Resmi (HDFS)

Memasukkan hasil ekstraksi data insiden (dari Wikipedia/PDF) ke HDFS untuk digunakan oleh modul `ml-nlp/validation`.
Sebagai alternatif ringan dari NiFi, kami menyediakan script Python yang melakukan interaksi langsung dengan HDFS di dalam Docker.

### Menjalankan Ingest Script
Pastikan container HDFS sudah berjalan (`docker-compose up -d namenode datanode`) dan file `incidents_full.csv` sudah di-generate di root folder.

```bash
# Jalankan dari root project
python data-engineering/nifi/ingest_incidents.py
```

Script ini akan:
1. Memvalidasi kelengkapan data CSV
2. Menyalin data ke container `nutriwatch-namenode`
3. Menyimpan data ke HDFS di path `/nutriwatch/incidents/raw/incidents_full.csv`
