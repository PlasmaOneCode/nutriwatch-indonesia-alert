# Handover Document: NutriWatch Indonesia Alert

**Dokumen ini ditujukan untuk agen AI selanjutnya agar dapat memahami konteks proyek, arsitektur, dan perubahan terbaru tanpa perlu membaca riwayat obrolan (chat history).**

## Konteks Proyek
**NutriWatch Indonesia Alert** adalah dasbor analitik dan peringatan dini (*Early Warning System*) berbasis Big Data untuk memantau sentimen publik dan risiko keracunan makanan dari program Makan Bergizi Gratis (MBG) yang dijalankan oleh pemerintah Indonesia. 

Sistem ini memproses jutaan cuitan (Twitter/X) menggunakan *Natural Language Processing* (NLP) model IndoBERT untuk mendeteksi sentimen negatif dan anomali, kemudian memvisualisasikannya di peta risiko dan dasbor secara *real-time*.

## Arsitektur Teknis
1. **Data Ingestion**: Apache Kafka & Apache NiFi memuat data mentah (CSV/API).
2. **Stream Processing**: Apache Spark Streaming membaca dari Kafka, memproses teks, menjalankan model NLP IndoBERT dan *Isolation Forest* untuk mendeteksi sinyal anomali.
3. **Database**: Elasticsearch menyimpan hasil deteksi dari Spark.
4. **Backend**: Flask API (`api/app.py`) menyajikan *endpoint* data ke *frontend*.
5. **Frontend**: React.js dengan TypeScript, menggunakan Tailwind CSS, React Query, dan Recharts (berada di folder `frontend/`).

---

## Perubahan dan Perbaikan Terbaru (Oleh Agen AI Sebelumnya)

Sebelumnya, proyek ini masih berupa purwarupa (*prototype*) yang menggunakan data *mock* (bohong-bohongan). Berikut adalah transformasi yang telah dilakukan untuk menjadikannya sistem *Live* dan dinamis:

### 1. Integrasi Live Elasticsearch (End-to-End)
- **Spark to ES (`big-data-processing/spark/streaming_job.py`)**: Skrip Spark Streaming telah dimodifikasi agar tidak lagi hanya mencetak hasil ke konsol. Sekarang, hasil NLP disuntikkan secara *real-time* ke indeks `signal_events` di Elasticsearch menggunakan metode `foreachBatch`.
- **Flask to ES (`api/app.py`)**: Seluruh *endpoint* API (`/api/stats`, `/api/signals`, `/api/aspects`, `/api/incidents`) telah dirombak untuk berhenti mengirimkan data statis. Mereka sekarang melakukan *Aggregate Query* ke Elasticsearch untuk mendapatkan jumlah sinyal `Critical`, `Warning`, dan sentimen secara akurat.
- **Bug Fix Versi Elasticsearch**: Terdapat masalah kompatibilitas (mendapat `BadRequestError`) karena `elasticsearch-py` versi 9 tidak cocok dengan *cluster* ES lokal pengguna (versi 8/7). Masalah ini diselesaikan dengan melakukan *downgrade* `pip install "elasticsearch<9"`.

### 2. Revamp Frontend Dinamis
- **Pembersihan Fitur**: Halaman statis `reports.tsx` telah dihapus sepenuhnya beserta menu navigasinya dari `Header.tsx` untuk menyederhanakan antarmuka.
- **Map View & Alerts (`map.tsx`, `alerts.tsx`)**: Komponen ini sekarang menggunakan *hooks* dari React Query (`useIncidents` & `useSignals`) untuk mengkalkulasi statistik ringkasan dan mewarnai peta geografis secara dinamis berdasarkan data Elasticsearch dari *backend*.
- **Penghapusan Placeholder**: Teks narasi di Beranda (`index.tsx`) yang sebelumnya menggunakan "Lorem Ipsum" telah diganti dengan narasi aktual mengenai latar belakang proyek MBG.

### 3. Integrasi Berita Nasional Real-time (`/api/news`)
- **Backend (Bing News RSS)**: Dibuat *endpoint* baru di `api/app.py` yang menggunakan `feedparser` untuk membaca RSS Bing News dengan kata kunci "Makan Bergizi Gratis Keracunan".
- **Bypass Keamanan (Anti 403 & Redirects)**: Sistem berhasil mengekstrak tautan artikel asli dari *URL redirect* milik Bing. Kemudian, skrip menyamar menggunakan *User-Agent* peramban asli dan menyedot gambar *thumbnail* asli (`<meta property="og:image">`) dari situs web bersangkutan (misal: Tempo, Liputan6) menggunakan `BeautifulSoup`.
- **Frontend**: Kartu berita di beranda sekarang tidak lagi menggunakan gambar statis (seperti `article1.png`), melainkan memuat langsung nama domain asal penerbit, ringkasan teks asli, dan gambar jurnalistik sungguhan dari API.

## Catatan Penting untuk AI Selanjutnya
- **Dependencies**: Modul seperti `feedparser`, `beautifulsoup4`, dan `elasticsearch<9` telah terinstal.
- **Docker**: Pastikan kontainer Elasticsearch berjalan di sistem pengguna sebelum mengeksekusi `streaming_job.py` atau mengakses API.
- **Spark**: Pekerjaan Spark Streaming cukup berat di awal muatan (butuh memuat model PyTorch ratusan MB), jadi wajar jika *batch* pertama memakan waktu sekitar satu menit sebelum data mulai mengalir ke Elasticsearch.

Gunakan dokumen ini sebagai pijakan dasar. Anda bisa langsung memulai tugas baru yang diberikan oleh pengguna dari titik ini. Semoga berhasil!
