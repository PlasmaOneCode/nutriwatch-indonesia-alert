# NutriWatch: Big Data-Driven Early Warning System untuk Deteksi Dini Risiko Keracunan Massal pada Program Makan Bergizi Gratis (MBG)

<div align="center">
  <!-- Logo Proyek -->
  <img width="180" alt="NutriWatch Logo" src="https://github.com/user-attachments/assets/e1ab8a15-8920-47f0-8ad3-c42d1d35f64a" />
  <br><br>
  <!-- Barisan Badges Baris 1 -->
  <a href="https://react.dev/"><img src="https://img.shields.io/badge/Framework-React%2018-blue?style=flat-square&logo=react" alt="Framework - React"></a>
  <a href="https://tailwindcss.com/"><img src="https://img.shields.io/badge/Styling-TailwindCSS-38B2AC?style=flat-square&logo=tailwind-css" alt="Styling - TailwindCSS"></a>
  <a href="https://leafletjs.com/"><img src="https://img.shields.io/badge/Maps-OSM%20%26%20Leaflet-green?style=flat-square&logo=openstreetmap" alt="Maps - OpenStreetMap"></a>
  <img src="https://img.shields.io/badge/Build-passing-brightgreen?style=flat-square" alt="Build - Passing">
  <img src="https://img.shields.io/badge/codecov-77%25-orange?style=flat-square" alt="Codecov">
  <br>
  <!-- Barisan Badges Baris 2 -->
  <img src="https://img.shields.io/badge/Documentation-v1.0-blue?style=flat-square" alt="Documentation">
  <img src="https://img.shields.io/badge/Open%20in-Colab-yellow?style=flat-square&logo=googlecolab" alt="Open in Colab">
  <img src="https://img.shields.io/badge/Discord-Community-7289DA?style=flat-square&logo=discord" alt="Discord">
</div>

---

### 📌 Latar Belakang

Pelaksanaan Program Makan Bergizi Gratis (MBG) skala nasional merupakan pilar strategis pemerintah untuk meningkatkan kualitas SDM. Namun, dalam implementasi awalnya, ekosistem MBG menghadapi tantangan multidimensional di lapangan yang mengancam keberlangsungan program serta keselamatan penerima manfaat. Permasalahan nyata tersebut meliputi kasus keracunan massal di berbagai daerah (seperti data yang dihimpun dari Wikipedia dan portal berita resmi).

NutriWatch hadir sebagai solusi proaktif (*Early Warning System*) yang memanfaatkan pemrosesan Big Data. Sistem ini menghubungkan data dinamis berupa keluhan masyarakat di media sosial (simulasi data streaming Twitter) dengan riwayat insiden resmi. Melalui analisis sentimen dan ekstraksi aspek, potensi penurunan kualitas makanan (misalnya higienitas atau porsi) dapat dideteksi sejak dini sebelum terjadi eskalasi kasus keracunan massal yang lebih parah.

---

## 🚀 Penjelasan Aplikasi

NutriWatch adalah aplikasi pemantauan berbasis Big Data yang mengintegrasikan lapisan pemrosesan data bervolume tinggi dengan machine learning NLP. Arsitektur sistem ini menggunakan:
1. **Data Ingestion**: Apache Kafka untuk mereplay dataset teks/tweet sebagai data *streaming* real-time, dan Python Script untuk ingest rekaman insiden CSV ke HDFS.
2. **Big Data Processing**: Apache Spark Structured Streaming untuk memproses teks secara paralel dan mengekstrak fitur harian (time windows) berdasarkan rasio sentimen negatif.
3. **ML & NLP**: Model Zero-Shot IndoBERT (mDeBERTa) digunakan untuk *Aspect-Based Sentiment Analysis* (ABSA) mengklasifikasikan keluhan ke 4 aspek utama (rasa, porsi, distribusi, higienitas). Pendekatan Zero-Shot ini diambil untuk mengoptimalkan batasan VRAM 4GB. Selain itu, digunakan *Isolation Forest* untuk mendeteksi sinyal anomali, serta *Lag Evaluator* untuk memvalidasi seberapa akurat sinyal memprediksi insiden nyata.
4. **Database & API**: Hadoop Distributed File System (HDFS) untuk menyimpan raw data, dan Elasticsearch untuk mengindeks data agregasi yang sudah bersih. Terdapat backend Flask REST API untuk menjembatani Elasticsearch dengan aplikasi Frontend.
5. **Frontend**: Dasbor interaktif berbasis React dan Tailwind CSS untuk visualisasi peta risiko dan tren sentimen secara real-time.

Semua infrastruktur dijalankan menggunakan *Docker Compose* secara lokal.

---

## 👥 Anggota Tim & Kontribusi

| No. | Nama | NRP | Peran Kelompok | Tanggung Jawab Teknis Utama |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Muhammad Huda Rabbani | 5027241098 | Lead Data Engineer | Mengembangkan script *data extraction* insiden (Scraping Wikipedia/PDF ke CSV), *Kafka Producer* untuk replay streaming dataset, dan script Python ingestion *batch* ke HDFS. |
| 2 | Muhammad Fachry Shalahuddin Rusamsi | 5027241031 | Big Data Developer | Mengembangkan pemrosesan inti pada *Apache Spark Streaming*; memanggil model ABSA sebagai UDF, lalu mengekstrak *feature windows* harian dan mengeksekusi deteksi anomali. |
| 3 | Muhammad Khairul Yahya | 5027241092 | ML & NLP Specialist | Mengimplementasikan model *Zero-Shot Classification* IndoBERT untuk Aspect-Based Sentiment Analysis dan mengembangkan algoritma *Isolation Forest* & *Lag Evaluator* menggunakan scikit-learn/pandas. |
| 4 | Daniswara Fausta Novanto | 5027241050 | Database & Storage Engineer | Mengonfigurasi arsitektur lokal via `docker-compose.yml` (Zookeeper, Kafka, Namenode, Datanode, Elasticsearch). Menyusun *mapping* skema indeks Elasticsearch dan HDFS. |
| 5 | Abiyyu Raihan Putra Wikanto | 5027241042 | UI/UX & Frontend Dev | Membangun dashboard monitoring interaktif berbasis React/Vite. Selain itu, juga merancang dan mengimplementasikan **Flask REST API** (`api/app.py`) sebagai perantara Frontend ke Backend. |

---

## 📁 Struktur Folder (Monorepo)

Repositori ini menggunakan struktur *monorepo* untuk memfasilitasi kolaborasi seluruh anggota tim ekosistem Big Data NutriWatch:

```text
├── /api                    # [Tugas Abiyyu] Flask REST API Wrapper (Endpoint /api/signals, /api/stats, dll)
├── /big-data-processing    # [Tugas Fachry] Apache Spark Streaming & Feature Extraction
├── /data-engineering       # [Tugas Huda] Pipeline Ingestion (Kafka Producer & HDFS Script) + Data Extraction CSV
├── /database-storage       # [Tugas Danis] Skema HDFS & Konfigurasi Mapping Elasticsearch
├── /frontend               # [Tugas Abiyyu] Aplikasi Dashboard React, Tailwind, & Leaflet Maps
├── /ml-nlp                 # [Tugas Irul] Model IndoBERT Zero-Shot, Anomaly Detection, & Lag Evaluator
├── docker-compose.yml      # Konfigurasi infrastruktur (Zookeeper, Kafka, Hadoop, Elasticsearch)
└── extract_incidents_from_pdf.py # Script awal untuk mengoleksi data resmi ke CSV
```

---

## 🛠️ Cara Menjalankan Aplikasi

Aplikasi ini menggunakan Docker untuk menjalankan komponen Big Data secara terisolasi.

### 1. Menjalankan Infrastruktur Dasar (Docker)
Pastikan Docker Desktop sudah aktif.
```bash
# Menyalakan seluruh service (Zookeeper, Kafka, Hadoop, Elasticsearch)
docker-compose up -d

# Mengecek status container
docker-compose ps
```

### 2. Frontend & API Backend
Jalankan Flask API dan React Server secara paralel.
```bash
# Terminal 1: Menjalankan Flask API
pip install flask flask-cors
python api/app.py
# API akan berjalan di http://localhost:5000

# Terminal 2: Menjalankan Frontend
cd frontend
npm install
npm run dev
# Dashboard akan berjalan di http://localhost:5173
```

### 3. Pipeline Data Engineering (Ingestion)
Untuk mensimulasikan aliran data teks dan insiden, jalankan script berikut:
```bash
# Ingest data insiden CSV historis ke dalam node HDFS
python data-engineering/nifi/ingest_incidents.py

# Mensimulasikan data streaming teks (mensyaratkan dataset kaggle di datasets/mbg_tweets.csv)
pip install kafka-python-ng pyyaml pandas
python data-engineering/kafka/producer.py
```

### 4. Big Data Processing & ML 
Menjalankan job Spark untuk memproses teks dari Kafka dan menghasilkan sinyal anomali.
```bash
# Pastikan pyspark, scikit-learn, transformers, dan torch terinstall
pip install pyspark findspark scikit-learn torch transformers pandas

# Menjalankan Spark Streaming 
python big-data-processing/spark/streaming_job.py

# (Alternatif) Test run feature extraction & model anomali secara terpisah
python big-data-processing/spark/feature_extractor.py
python ml-nlp/validation/lag_evaluator.py
```
