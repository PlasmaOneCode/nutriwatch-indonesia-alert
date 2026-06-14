# NutriWatch: Big Data-Driven Early Warning System untuk Ekosistem Program Makan Bergizi Gratis (MBG)

<!-- Badges Section (Inspirasi dari image_3a10c2.png) -->
[![Framework - React](https://img.shields.io/badge/Framework-React%2018-blue?style=flat-square&logo=react)](https://react.dev/)
[![Styling - TailwindCSS](https://img.shields.io/badge/Styling-TailwindCSS-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)
[![Maps - OpenStreetMap](https://img.shields.io/badge/Maps-OSM%20%26%20Leaflet-green?style=flat-square&logo=openstreetmap)](https://leafletjs.com/)
[![Build - Passing](https://img.shields.io/badge/Build-passing-brightgreen?style=flat-square)](#)
[![Codecov](https://img.shields.io/badge/codecov-77%25-orange?style=flat-square)](#)
<br>
[![Documentation](https://img.shields.io/badge/Documentation-v1.0-blue?style=flat-square)](#)
[![Open in Colab](https://img.shields.io/badge/Open%20in-Colab-yellow?style=flat-square&logo=googlecolab)](#)
[![Discord](https://img.shields.io/badge/Discord-Community-7289DA?style=flat-square&logo=discord)](#)

---

## 📌 Latar Belakang

Pelaksanaan Program Makan Bergizi Gratis (MBG) skala nasional merupakan pilar strategis pemerintah untuk meningkatkan kualitas SDM[cite: 1]. Namun, implementasi di lapangan menghadapi tantangan multidimensional mulai dari krisis kesehatan berupa insiden keracunan massal, rendahnya standarisasi sanitasi dapur umum (HACCP), keterlambatan pencairan anggaran vendor, hingga kendala distribusi di wilayah 3T[cite: 1]. Sistem pengawasan yang ada saat ini umumnya bersifat reaktif, di mana investigasi baru berjalan setelah jatuhnya korban[cite: 1].

NutriWatch hadir sebagai solusi proaktif (*Early Warning System*) yang memanfaatkan teknik fusi data (*data fusion*) skala besar[cite: 1]. Sistem ini secara cerdas mengorelasikan data statis finansial operasional dengan aliran data dinamis berupa keluhan masyarakat di media sosial secara *real-time*[cite: 1]. Melalui pendekatan ini, potensi penurunan kualitas makanan akibat masalah *cashflow* dapur umum dapat dideteksi sejak dini sebelum terjadi eskalasi kasus keracunan massal[cite: 1].

---

## 🚀 Penjelasan Aplikasi

NutriWatch adalah aplikasi pemantauan berbasis Big Data yang mengintegrasikan lapisan pemrosesan data bervolume tinggi dengan kecerdasan buatan untuk mengawal ekosistem MBG[cite: 1]. Arsitektur sistem ini mengandalkan Apache Kafka dan Apache NiFi untuk *data ingestion*, serta Apache Spark Streaming sebagai mesin pemrosesan inti untuk menggabungkan data operasional dan data sentimen publik[cite: 1]. Analisis teks dilakukan secara mendalam menggunakan model Deep Learning IndoBERT untuk *Aspect-Based Sentiment Analysis* (ABSA) guna memetakan keluhan pada aspek spesifik seperti kesehatan, anggaran, logistik, dan kualitas dapur[cite: 1].

Pada sisi antarmuka, NutriWatch menyajikan dasbor monitoring interaktif tingkat *enterprise* yang dibangun menggunakan React dan Tailwind CSS[cite: 1]. Fitur utama dasbor ini meliputi visualisasi peta risiko spasial interaktif berbasis OpenStreetMap (OSM) dan React-Leaflet untuk memetakan zonasi aman hingga darurat dapur umum, visualisasi persentase sentimen aspek, serta sistem notifikasi otomatis *Red Flag* yang menyala secara *real-time* ketika indikasi bahaya keracunan terdeteksi oleh sistem inti[cite: 1].

---

## 📁 Struktur Folder (Monorepo)

Repositori ini menggunakan struktur *monorepo* untuk memfasilitasi kolaborasi seluruh anggota tim ekosistem Big Data NutriWatch[cite: 1]:

```text
├── /frontend               # [Tugas Abiyyu] Aplikasi Dashboard React, Tailwind, & Leaflet Maps
├── /data-engineering       # [Tugas Daniswara] Pipeline Ingestion (Apache Kafka & Apache NiFi)
├── /big-data-processing    # [Tugas Fachry] Core Processing Scripts (Apache Spark Streaming)
├── /ml-nlp                 # [Tugas Irul] Model IndoBERT (ABSA) & Isolation Forest
└── /database-storage       # [Tugas Huda] Konfigurasi Cluster HDFS & Indexing Elasticsearch

```

---

## 🛠️ Cara Menjalankan Aplikasi

### 1. Frontend & UI/UX Dashboard (Bagian Abiyyu)

Bagian ini berisi aplikasi dasbor pemantauan berbasis React yang dikembangkan melalui Lovable AI.

**Prasyarat:** Ensure you have [Node.js](https://nodejs.org/) installed (v18 or higher recommended).

```bash
# Masuk ke direktori frontend
cd frontend

# Install semua dependencies (termasuk Tailwind, Lucide Icons, dan React-Leaflet)
npm install

# Jalankan server lokal untuk development
npm run dev

```

Setelah dijalankan, buka tautan `http://localhost:5173` (atau port yang tertera pada terminal) di browser Anda.

### 2. Data Ingestion Pipeline

> ⚠️ **[PLACEHOLDER]** *Akan diperbarui oleh Lead Data Engineer untuk konfigurasi script producer/consumer Apache Kafka dan flow Apache NiFi.*

### 3. Big Data Processing Core 

> ⚠️ **[PLACEHOLDER]** *Akan diperbarui oleh Big Data Developer untuk instruksi penyerahan script Apache Spark (submit job) dan transformasi data.*

### 4. ML & NLP Models 

> ⚠️ **[PLACEHOLDER]** *Akan diperbarui oleh ML & NLP Specialist untuk cara memuat model IndoBERT fine-tuned dan deteksi Isolation Forest.*

### 5. Database & Storage Layer 

> ⚠️ **[PLACEHOLDER]** *Akan diperbarui oleh Database Engineer untuk skema pemetaan indeks Elasticsearch dan konfigurasi node HDFS.*

---

*Hak Cipta © 2026 Tim NutriWatch Big Data Ecosystem.*

```
