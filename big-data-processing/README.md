# Big Data Processing Module — NutriWatch

Modul ini bertanggung jawab untuk memproses stream data teks dari Kafka, mengekstrak informasi sentimen menggunakan model NLP, lalu membuat window agregasi harian.

## Komponen

### 1. Spark Streaming Job (`spark/streaming_job.py`)
Membaca data dari topic Kafka `mbg-text-stream`, menerapkan pemrosesan NLP (ABSA) menggunakan UDF (User Defined Function), dan menyimpannya.
*Catatan: Saat ini script dikonfigurasi untuk menampilkan hasil ke Console untuk keperluan MVP/Testing. Untuk menulis ke HDFS, uncomment bagian HDFS `writeStream`.*

### 2. Feature Extractor (`spark/feature_extractor.py`)
Fungsi Python biasa (bisa dijalankan sebagai pandas atau PySpark batch job) yang mengambil hasil mentah dari Spark, mengagregasinya menjadi fitur window harian (`tweet_volume`, `negative_ratio`, `dominant_aspect`), dan memanggil detektor anomali Isolation Forest untuk menemukan sinyal.

## Menjalankan Spark Streaming (MVP / Local)

Pastikan layanan Kafka sudah berjalan via Docker.

**Install Pyspark & Kafka Source Jar:**
```bash
# Pastikan pyspark dan findspark terinstall
pip install pyspark findspark
```

**Run Streaming Job:**
```bash
# Di root direktori project
python big-data-processing/spark/streaming_job.py
```
*(Saat dijalankan, Spark akan mendownload package org.apache.spark:spark-sql-kafka-0-10_2.12 secara otomatis)*

**Run Feature Extractor Testing:**
```bash
python big-data-processing/spark/feature_extractor.py
```
