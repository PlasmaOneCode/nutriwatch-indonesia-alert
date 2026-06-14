# NutriWatch: Big Data-Driven Early Warning System untuk Ekosistem Program Makan Bergizi Gratis (MBG)

<p align="center">
  <a href="https://react.dev/"><img src="https://img.shields.io/badge/Framework-React%2018-blue?style=flat-square&logo=react" alt="Framework - React"></a>
  <a href="https://tailwindcss.com/"><img src="https://img.shields.io/badge/Styling-TailwindCSS-38B2AC?style=flat-square&logo=tailwind-css" alt="Styling - TailwindCSS"></a>
  <a href="https://leafletjs.com/"><img src="https://img.shields.io/badge/Maps-OSM%20%26%20Leaflet-green?style=flat-square&logo=openstreetmap" alt="Maps - OpenStreetMap"></a>
  <img src="https://img.shields.io/badge/Build-passing-brightgreen?style=flat-square" alt="Build - Passing">
  <img src="https://img.shields.io/badge/codecov-77%25-orange?style=flat-square" alt="Codecov">
  <br>
  <img src="https://img.shields.io/badge/Documentation-v1.0-blue?style=flat-square" alt="Documentation">
  <img src="https://img.shields.io/badge/Open%20in-Colab-yellow?style=flat-square&logo=googlecolab" alt="Open in Colab">
  <img src="https://img.shields.io/badge/Discord-Community-7289DA?style=flat-square&logo=discord" alt="Discord">
</p>

---

## 📌 Latar Belakang

Pelaksanaan Program Makan Bergizi Gratis (MBG) skala nasional merupakan pilar strategis pemerintah untuk meningkatkan kualitas SDM. Namun, dalam implementasi awalnya, ekosistem MBG menghadapi tantangan multidimensional di lapangan yang mengancam keberlangsungan program serta keselamatan penerima manfaat. Permasalahan nyata tersebut dapat dikategorikan ke dalam empat klaster utama: krisis kesehatan (kasus keracunan massal), masalah standarisasi dapur (HACCP), anomali finansial & operasional (keterlambatan dana vendor), serta ketimpangan distribusi di wilayah 3T.

NutriWatch hadir sebagai solusi proaktif (*Early Warning System*) yang memanfaatkan teknik fusi data (*data fusion*) skala besar. Sistem ini secara cerdas mengorelasikan data statis finansial operasional dengan aliran data dinamis berupa keluhan masyarakat di media sosial secara *real-time*. Melalui pendekatan ini, potensi penurunan kualitas makanan akibat masalah *cashflow* dapur umum dapat dideteksi sejak dini sebelum terjadi eskalasi kasus keracunan massal.

---

## 🚀 Penjelasan Aplikasi

NutriWatch adalah aplikasi pemantauan berbasis Big Data yang mengintegrasikan lapisan pemrosesan data bervolume tinggi dengan kecerdasan buatan untuk mengawal ekosistem MBG. Arsitektur sistem ini mengandalkan Apache Kafka dan Apache NiFi untuk *data ingestion*, serta Apache Spark Streaming sebagai mesin pemrosesan inti untuk menggabungkan data operasional dan data sentimen publik. Analisis teks dilakukan secara mendalam menggunakan model Deep Learning IndoBERT untuk *Aspect-Based Sentiment Analysis* (ABSA) guna memetakan keluhan pada aspek spesifik seperti kesehatan, anggaran, logistik, dan kualitas dapur.

Pada sisi antarmuka, NutriWatch menyajikan dasbor monitoring interaktif tingkat *enterprise* yang dibangun menggunakan React dan Tailwind CSS. Fitur utama dasbor ini meliputi visualisasi peta risiko spasial interaktif berbasis OpenStreetMap (OSM) dan React-Leaflet untuk memetakan zonasi aman hingga darurat dapur umum, visualisasi persentase sentimen aspek, serta sistem notifikasi otomatis *Red Flag* yang menyala secara *real-time* ketika indikasi bahaya keracunan terdeteksi oleh sistem inti.

---

## 👥 Anggota Tim & Kontribusi

| No. | Nama | NRP | Peran Kelompok | Tanggung Jawab Teknis Utama |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Daniswara Fausta Novanto | 5027241050 | Lead Data Engineer | Membangun arsitektur pipeline data menggunakan Apache Kafka dan Apache NiFi; bertanggung jawab atas kelancaran ingestion data dari sumber eksternal ke cluster pemrosesan. |
| 2 | Muhammad Fachry Shalahuddin Rusamsi | 5027241031 | Big Data Developer | Mengembangkan skrip pemrosesan inti pada Apache Spark Streaming; melakukan transformasi, pembersihan data masif, dan penggabungan (data join) antar-dataset operasional. |
| 3 | Muhammad Khairul Yahya | 5027241092 | ML & NLP Specialist | Melatih model IndoBERT untuk Aspect-Based Sentiment Analysis; mengembangkan skrip deteksi anomali anggaran menggunakan algoritma machine learning (scikit-learn/PyTorch). |
| 4 | Muhammad Huda Rabbani | 5027241098 | Database & Storage Engineer | Mengonfigurasi klaster HDFS dan mengoptimalkan indeks pencarian pada Elasticsearch; memastikan retensi data aman dan kueri dashboard berjalan dengan latensi rendah. |
| 5 | Abiyyu Raihan Putra Wikanto | 5027241042 | UI/UX & Frontend Dev | Membangun dashboard monitoring interaktif (Grafana/React); mengintegrasikan visualisasi peta risiko (geospatial), sistem notifikasi red-flag, dan penyusunan dokumen laporan. |

---

## 📁 Struktur Folder (Monorepo)

Repositori ini menggunakan struktur *monorepo* untuk memfasilitasi kolaborasi seluruh anggota tim ekosistem Big Data NutriWatch:

```text
├── /frontend               # [Tugas Abiyyu] Aplikasi Dashboard React, Tailwind, & Leaflet Maps
├── /data-engineering       # [Tugas Daniswara] Pipeline Ingestion (Apache Kafka & Apache NiFi)
├── /big-data-processing    # [Tugas Fachry] Core Processing Scripts (Apache Spark Streaming)
├── /ml-nlp                 # [Tugas Irul] Model IndoBERT (ABSA) & Isolation Forest
└── /database-storage       # [Tugas Huda] Konfigurasi Cluster HDFS & Indexing Elasticsearch

```

---

## 🛠️ Cara Menjalankan Aplikasi

### 1. Frontend & UI/UX Dashboard 

Bagian ini berisi aplikasi dasbor pemantauan berbasis React yang dikembangkan melalui Lovable AI.

**Prasyarat:** Pastikan Anda sudah menginstal [Node.js](https://nodejs.org/) (Direkomendasikan v18 atau versi di atasnya).

```bash
# Masuk ke direktori frontend
cd frontend

# Install semua dependencies (termasuk Tailwind, Lucide Icons, dan React-Leaflet)
npm install

# Jalankan server lokal untuk development
npm run dev

```

Setelah dijalankan, buka tautan `http://localhost:5173` (atau nomor port lain yang tertera pada terminal Anda) di browser.

### 2. Data Ingestion Pipeline 

> ⚠️ **[PLACEHOLDER]** *Akan diperbarui oleh Lead Data Engineer untuk konfigurasi script producer/consumer Apache Kafka dan flow Apache NiFi.*

### 3. Big Data Processing Core 

> ⚠️ **[PLACEHOLDER]** *Akan diperbarui oleh Big Data Developer untuk instruksi penyerahan script Apache Spark (submit job) dan transformasi data.*

### 4. ML & NLP Models 

> ⚠️ **[PLACEHOLDER]** *Akan diperbarui oleh ML & NLP Specialist untuk cara memuat model IndoBERT fine-tuned dan deteksi Isolation Forest.*

### 5. Database & Storage Layer 

> ⚠️ **[PLACEHOLDER]** *Akan diperbarui oleh Database Engineer untuk skema pemetaan indeks Elasticsearch dan konfigurasi node HDFS.*

