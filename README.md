# NutriWatch: Big Data-Driven Early Warning System untuk Deteksi Dini Risiko Keracunan Massal pada Program Makan Bergizi Gratis (MBG)

<div align="center">
  <!-- Logo Proyek -->
  <img width="180" alt="NutriWatch Logo" src="https://github.com/user-attachments/assets/e1ab8a15-8920-47f0-8ad3-c42d1d35f64a" />
  <br><br>
  <!-- Barisan Badges Baris 1 -->
  <a href="https://react.dev/"><img src="https://img.shields.io/badge/Frontend-React%2018-blue?style=flat-square&logo=react" alt="Frontend - React"></a>
  <a href="https://tailwindcss.com/"><img src="https://img.shields.io/badge/Styling-TailwindCSS-38B2AC?style=flat-square&logo=tailwind-css" alt="Styling - TailwindCSS"></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Backend-Flask-black?style=flat-square&logo=flask" alt="Backend - Flask"></a>
  <br>
  <!-- Barisan Badges Baris 2 -->
  <a href="https://spark.apache.org/"><img src="https://img.shields.io/badge/Processing-Apache%20Spark-E25A1C?style=flat-square&logo=apachespark" alt="Processing - Spark"></a>
  <a href="https://kafka.apache.org/"><img src="https://img.shields.io/badge/Ingestion-Apache%20Kafka-231F20?style=flat-square&logo=apachekafka" alt="Ingestion - Kafka"></a>
  <a href="https://www.elastic.co/"><img src="https://img.shields.io/badge/Database-Elasticsearch-005571?style=flat-square&logo=elasticsearch" alt="Database - Elasticsearch"></a>
  <a href="https://pytorch.org/"><img src="https://img.shields.io/badge/ML-PyTorch-EE4C2C?style=flat-square&logo=pytorch" alt="ML - PyTorch"></a>
</div>

---

### 📌 Latar Belakang

Pelaksanaan Program Makan Bergizi Gratis (MBG) skala nasional merupakan pilar strategis pemerintah untuk meningkatkan kualitas SDM. Namun, dalam implementasi awalnya, ekosistem MBG menghadapi tantangan multidimensional di lapangan yang mengancam keberlangsungan program serta keselamatan penerima manfaat. Permasalahan nyata tersebut meliputi kasus keracunan massal di berbagai daerah (seperti data yang dihimpun dari portal berita resmi).

NutriWatch hadir sebagai solusi proaktif (*Early Warning System*) yang memanfaatkan pemrosesan Big Data. Sistem ini menghubungkan data dinamis berupa keluhan masyarakat di media sosial dengan riwayat insiden resmi. Melalui analisis sentimen dan ekstraksi aspek, potensi penurunan kualitas makanan (misalnya higienitas atau porsi) dapat dideteksi sejak dini sebelum terjadi eskalasi kasus keracunan massal yang lebih parah.

---

## 🚀 Alur Pemrosesan Data (Data Pipeline Flow)

Sistem NutriWatch dirancang dengan arsitektur data streaming end-to-end:
1. **Data Ingestion (Hulu)**: Data media sosial (simulasi cuitan) dipompa secara *real-time* ke **Apache Kafka** oleh Kafka Producer.
2. **Stream Processing (Tengah)**: **Apache Spark Streaming** membaca aliran data dari Kafka. Setiap teks keluhan diklasifikasikan menggunakan NLP (IndoBERT mDeBERTa) ke 4 aspek (rasa, porsi, distribusi, higienitas). Kemudian, algoritma *Isolation Forest* mengidentifikasi mana cuitan yang merupakan anomali bahaya (*Critical Signal*).
3. **Data Storage (Hilir)**: Hasil agregasi Spark langsung diindeks (*sink*) ke dalam **Elasticsearch**.
4. **Backend API**: **Flask REST API** bertugas menanyakan (*query*) data statistik dan daftar sinyal bahaya ke Elasticsearch. API ini juga mengambil artikel berita terkini dari web via modul *scraping*.
5. **Dashboard Visualisasi**: **React Frontend** menarik data dari Flask API dan memvisualisasikannya ke bentuk Dasbor Interaktif (Peta Geografis, Peringatan Langsung, dan Tren Grafik).

---

## 👥 Anggota Tim & Kontribusi

| No. | Nama | NRP | Peran Kelompok | Tanggung Jawab Teknis Utama |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Muhammad Huda Rabbani | 5027241098 | Lead Data Engineer | Mengembangkan *Kafka Producer* untuk *replay streaming dataset*, dan script Python ingestion *batch* ke HDFS. |
| 2 | Muhammad Fachry Shalahuddin Rusamsi | 5027241031 | Big Data Developer | Mengembangkan pemrosesan inti pada *Apache Spark Streaming*; memanggil model ABSA, lalu mengekstrak *feature windows* dan mendeteksi anomali. |
| 3 | Muhammad Khairul Yahya | 5027241092 | ML & NLP Specialist | Mengimplementasikan model *Zero-Shot Classification* IndoBERT untuk Aspect-Based Sentiment Analysis dan mengembangkan algoritma *Isolation Forest*. |
| 4 | Daniswara Fausta Novanto | 5027241050 | Database Engineer | Mengonfigurasi arsitektur lokal via `docker-compose.yml` (Zookeeper, Kafka, Hadoop, Elasticsearch). |
| 5 | Abiyyu Raihan Putra Wikanto | 5027241042 | UI/UX & Backend | Membangun dashboard monitoring interaktif berbasis React/Vite dan mengembangkan **Flask REST API** sebagai jembatan sistem. |

---

## 📁 Struktur Folder (Monorepo)

Repositori ini menggunakan struktur *monorepo* untuk memfasilitasi kolaborasi ekosistem Big Data NutriWatch:

```text
├── /api                    # Flask REST API Wrapper
├── /big-data-processing    # Apache Spark Streaming & Feature Extraction
├── /data-engineering       # Pipeline Ingestion (Kafka Producer & HDFS Script)
├── /database-storage       # Konfigurasi Mapping Elasticsearch
├── /frontend               # Aplikasi Dashboard React, Tailwind, & Leaflet Maps
├── /ml-nlp                 # Model IndoBERT Zero-Shot & Anomaly Detection
├── docker-compose.yml      # Konfigurasi infrastruktur (Kafka, Elasticsearch, dll)
└── README.md               # Dokumentasi Proyek
```

---

## 🛠️ Instruksi Menjalankan Aplikasi

Aplikasi ini menggunakan Docker untuk menjalankan komponen Big Data secara terisolasi.

### 1. Menjalankan Infrastruktur Dasar (Docker)
Pastikan Docker Desktop sudah aktif.
```bash
# Menyalakan seluruh service (Zookeeper, Kafka, Elasticsearch, dll)
docker-compose up -d

# Mengecek status container
docker-compose ps
```

### 2. Frontend & API Backend
Jalankan Flask API dan React Server secara paralel.
```bash
# Terminal 1: Menyiapkan dan Menjalankan Flask API
pip install flask flask-cors feedparser beautifulsoup4 "elasticsearch<9"
python api/app.py
# API akan berjalan di http://localhost:5000

# Terminal 2: Menyiapkan dan Menjalankan Frontend
cd frontend
npm install
npm run dev
# Dashboard akan berjalan di http://localhost:8080 (atau port lain yang dialokasikan Vite)
```

### 3. Pipeline Data Engineering (Ingestion Kafka)
Untuk memompa data aliran media sosial secara langsung ke Spark:
```bash
# Terminal 3: Menjalankan Kafka Producer
pip install kafka-python-ng pyyaml pandas
python data-engineering/kafka/producer.py
```

### 4. Big Data Processing (Spark Streaming)
Menjalankan job Spark untuk memproses teks dari Kafka secara *real-time* dan mengirim hasilnya ke Elasticsearch.
```bash
# Terminal 4: Menjalankan Apache Spark Streaming
# Pastikan library terinstall
pip install pyspark findspark scikit-learn torch transformers pandas "elasticsearch<9"

# Jalankan skrip pemrosesan
python big-data-processing/spark/streaming_job.py
```
*(Catatan: Batch pertama Spark membutuhkan waktu sekitar satu menit untuk memuat model NLP sebelum dapat menampilkan data).*
