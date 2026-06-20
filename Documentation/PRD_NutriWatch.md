# PRD: NutriWatch
## Big Data-Driven Early Warning System untuk Deteksi Dini Risiko Keracunan Massal pada Program Makan Bergizi Gratis (MBG)

**Status dokumen:** Final untuk eksekusi
**Repo:** https://github.com/PlasmaOneCode/nutriwatch-indonesia-alert
**Catatan untuk AI/developer yang melanjutkan:** Dokumen ini ditulis agar bisa langsung dieksekusi tanpa konteks tambahan dari percakapan sebelumnya. Setiap istilah teknis didefinisikan secara eksplisit di Bagian 5 dan Lampiran. Jangan mengasumsikan konteks di luar yang tertulis di sini.

---

## 1. Ringkasan Proyek

NutriWatch adalah pipeline Big Data yang memantau opini publik terkait Program Makan Bergizi Gratis (MBG) di media sosial, mendeteksi lonjakan keluhan yang tidak normal (disebut **sinyal dini**), dan membandingkan waktu kemunculan sinyal tersebut dengan tanggal insiden keracunan massal yang tercatat resmi oleh otoritas. Tujuannya adalah menguji secara empiris apakah opini publik bisa berfungsi sebagai indikator dini sebelum insiden keracunan dilaporkan secara resmi.

Proyek ini BUKAN sistem prediksi yang menjamin "akan terjadi keracunan". Proyek ini adalah sistem deteksi anomali statistik pada data teks publik, yang hasilnya divalidasi secara retrospektif terhadap data insiden resmi.

---

## 2. Latar Belakang & Urgensi

Program MBG mengalami banyak insiden keracunan massal sejak diluncurkan awal 2025. Badan Gizi Nasional (BGN) melaporkan rekapitulasi resmi sebanyak 4.711 kasus keracunan per 22 September 2025, dengan rincian tanggal kejadian, nama SPPG (dapur), lokasi, dan jumlah korban per kasus. Dari jumlah tersebut, BGN membagi pemantauan menjadi tiga wilayah administratif: Wilayah I (Sumatra), Wilayah II (Jawa), dan Wilayah III (Indonesia bagian timur). Wilayah II (Jawa) tercatat sebagai wilayah paling terdampak dengan 4.147 dari 4.711 kasus.

Saat ini, deteksi insiden hanya bersifat reaktif — otoritas baru mengetahui adanya masalah setelah laporan resmi dari sekolah/puskesmas masuk. Tidak ada mekanisme yang memantau sinyal keluhan publik di media sosial sebagai indikator dini sebelum eskalasi menjadi laporan resmi.

---

## 3. Rumusan Masalah & Tujuan

**Rumusan masalah:** Apakah lonjakan volume dan sentimen negatif pada opini publik terkait MBG di media sosial dapat berfungsi sebagai sinyal dini yang mendahului (atau setidaknya bersamaan dengan) pencatatan insiden keracunan resmi?

**Tujuan proyek:**
1. Membangun pipeline Big Data yang memproses data teks publik terkait MBG secara terstruktur (disimulasikan sebagai stream melalui dataset replay).
2. Mendeteksi window waktu dengan pola keluhan yang menyimpang signifikan dari baseline historis (sinyal dini).
3. Mengukur selisih waktu (lag) antara kemunculan sinyal dan tanggal insiden resmi tercatat di wilayah yang sama.
4. Menyajikan hasil dalam dashboard yang informatif tanpa mengklaim kemampuan prediksi yang tidak bisa dibuktikan.

---

## 4. Scope

### 4.1 In Scope (MVP)
- Wilayah geografis: **Wilayah II (Jawa)** saja — DKI Jakarta, Jawa Barat, Jawa Tengah, DI Yogyakarta, Jawa Timur, Banten.
- Sumber data: dataset teks publik (tweet/komentar) terkait MBG yang sudah ada di Kaggle, di-replay melalui Kafka untuk mensimulasikan streaming.
- Data insiden resmi: dikumpulkan dari sumber publik (rekapitulasi BGN/JPPI yang dipublikasikan media, serta Wikipedia), diekstrak menjadi dataset terstruktur (CSV) berisi tanggal, lokasi SPPG, dan jumlah korban.
- 4 aspek keluhan yang dianalisis: rasa & menu, porsi & kecukupan, distribusi & ketepatan waktu, higienitas & keamanan.
- Granularitas window: **harian** (per hari, per wilayah), karena data insiden resmi hanya memiliki resolusi tanggal (tidak ada jam pasti).
- Output: sinyal dini (anomaly flag) per hari, plus hasil validasi lag-time terhadap data insiden resmi.

### 4.2 Out of Scope (eksplisit tidak dikerjakan)
- **Tidak ada fitur form input atau submission manual dari pengguna eksternal.** Semua data masuk hanya dari dua jalur: dataset teks (replay) dan data insiden resmi (batch ingestion dari sumber publik yang sudah dipublikasikan).
- **Tidak ada scraping data live** dari media sosial atau API pihak ketiga. Semua data teks bersumber dari dataset Kaggle yang sudah ada, diputar ulang (replay) melalui Kafka untuk mensimulasikan kondisi streaming.
- **Tidak mencakup wilayah I dan III** (Sumatra dan Indonesia bagian timur) pada fase MVP ini. Bisa jadi pengembangan lanjutan, tapi bukan bagian dari deliverable final project.
- **Tidak ada korelasi dengan data finansial/anggaran dapur.** Versi proposal sebelumnya mencakup ini, tapi dihapus karena tidak ada dataset finansial MBG yang publik dan terpercaya.
- **Tidak mengklaim hubungan kausal.** Sistem hanya mengukur korelasi temporal (selisih waktu) antara sinyal dan insiden, bukan membuktikan bahwa keluhan publik MENYEBABKAN atau MEMPREDIKSI insiden secara pasti.
- **Tidak melakukan klasifikasi per dapur/SPPG individual.** Analisis dilakukan di level wilayah (Jawa), bukan per dapur, karena data teks publik tidak punya metadata lokasi yang cukup presisi untuk level dapur.

---

## 5. Definisi Operasional Kunci

Bagian ini WAJIB dibaca sebelum membangun komponen apa pun, karena mendefinisikan istilah yang dipakai di seluruh dokumen ini.

**Window**: satu satuan waktu analisis, didefinisikan sebagai 1 hari kalender. Semua agregasi fitur dihitung per window per wilayah.

**Fitur window**: tiga angka yang dihitung untuk setiap window:
- `tweet_volume`: jumlah teks publik terkait MBG dalam window tersebut.
- `negative_ratio`: persentase teks yang diklasifikasikan bersentimen negatif oleh model ABSA, dari total teks dalam window tersebut.
- `dominant_aspect`: aspek (dari 4 aspek yang didefinisikan di Bagian 4.1) yang paling banyak disebut sebagai keluhan dalam window tersebut.

**Sinyal dini (signal/anomaly)**: window yang kombinasi tiga fiturnya di atas dianggap menyimpang signifikan dari pola historis baseline, dideteksi menggunakan algoritma Isolation Forest yang dilatih secara unsupervised dari data historis window-window sebelumnya. Output: `anomaly_score` (skor kontinu 0–1, semakin tinggi semakin menyimpang) dan `is_signal` (boolean, true jika anomaly_score melewati ambang batas yang ditentukan dari parameter contamination Isolation Forest).

**PENTING — yang BUKAN trigger sinyal dini:** Berita atau laporan media TIDAK digunakan sebagai input untuk mendeteksi sinyal dini. Sinyal dini murni dihitung dari fitur window data teks publik (lihat di atas).

**Data insiden resmi**: dataset terpisah yang berisi tanggal, lokasi, dan jumlah korban dari insiden keracunan MBG yang sudah dipublikasikan otoritas (BGN/JPPI) atau dikompilasi media. Dataset ini TIDAK dipakai sebagai input untuk mendeteksi sinyal dini — dataset ini HANYA dipakai pada tahap validasi (lihat di bawah), untuk mengevaluasi performa sistem secara retrospektif.

**Validasi lag-time**: proses membandingkan setiap window dengan `is_signal = true` terhadap data insiden resmi pada wilayah yang sama. Untuk setiap sinyal pada tanggal `d`, sistem mengecek apakah ada insiden resmi tercatat dalam rentang `[d, d+7]` (7 hari ke depan dari tanggal sinyal) di Wilayah II. Jika ada, `lag_days = tanggal_insiden - tanggal_sinyal` (nilai positif berarti sinyal mendahului insiden). Jika tidak ada insiden dalam rentang itu, sinyal tersebut dianggap "tidak match" (kemungkinan false positive, atau insiden yang tidak tercatat publik).

**Match rate**: persentase insiden resmi yang punya minimal satu sinyal dini dalam rentang 7 hari sebelum tanggal insiden tersebut. Ini adalah metrik evaluasi utama proyek — bukan untuk membuktikan sistem "berhasil", tapi untuk melaporkan secara jujur seberapa kuat korelasi temporal yang ditemukan.

**Replay (dataset replay)**: teknik mengonsumsi dataset statis (sudah ada, bukan live) melalui Kafka Producer seolah-olah data masuk secara real-time, untuk keperluan demonstrasi arsitektur streaming. Ini BUKAN scraping live — sumber data tetap dataset historis yang sudah ada.

**4 Aspek ABSA**:
| Kode Aspek | Nama | Contoh kata kunci terkait |
|---|---|---|
| `rasa_menu` | Rasa & Menu | enak, hambar, aneh, variasi menu |
| `porsi_kecukupan` | Porsi & Kecukupan | porsi kecil, kurang, cukup, banyak |
| `distribusi_ketepatan` | Distribusi & Ketepatan Waktu | telat, terlambat, basi karena lama, dingin |
| `higienitas_keamanan` | Higienitas & Keamanan | bau, kotor, ulat, keracunan, mual, sakit perut |

---

## 6. Arsitektur Sistem

```
[Dataset teks MBG (Kaggle)]
         │
         ▼
[Kafka Producer — replay dataset sebagai stream]
         │
         ▼
[Spark Structured Streaming — windowing per hari per wilayah]
         │
         ├──► [IndoBERT ABSA — klasifikasi aspek + sentimen per teks]
         │
         ▼
[Feature Extractor — hitung tweet_volume, negative_ratio, dominant_aspect per window]
         │
         ▼
[Isolation Forest — hitung anomaly_score, tentukan is_signal]
         │
         ├──► [HDFS — simpan raw log teks + fitur window]
         │
         ▼
[Elasticsearch — index signal_events untuk query cepat]
         │
         ▼
[React Dashboard — tampilkan sinyal, aspek, statistik]

[Data insiden resmi (BGN/JPPI/Wikipedia, batch CSV)]
         │
         ▼
[NiFi — batch ingest ke HDFS]
         │
         ▼
[Lag-time Validator — bandingkan signal_events vs incident_records]
         │
         ▼
[Elasticsearch — index validation_results]
         │
         ▼
[React Dashboard — tampilkan match rate, lag time]
```

Dua jalur data (teks publik dan data insiden resmi) berjalan terpisah. Mereka hanya bertemu di komponen Lag-time Validator, yang dijalankan secara periodik (misalnya setiap kali ada window baru) untuk mengevaluasi performa, bukan untuk memengaruhi deteksi sinyal itu sendiri.

---

## 7. Sumber Data (Referensi Konseptual)

Detail link dataset dikelola secara terpisah oleh koordinator proyek (lihat dokumen referensi tambahan di luar PRD ini). Berikut deskripsi jenis data yang dibutuhkan setiap komponen — gunakan ini untuk memvalidasi apakah dataset yang diberikan koordinator sudah sesuai:

**A. Dataset Teks Publik MBG** (untuk Kafka replay + ABSA)
- Format: CSV/JSON berisi kolom teks (isi tweet/komentar), timestamp, dan idealnya metadata lokasi (meski sering tidak lengkap).
- Volume: ribuan baris (skala ribuan hingga puluhan ribu teks).
- Bahasa: Bahasa Indonesia (dengan campuran bahasa daerah/gaul).

**B. Dataset Insiden Resmi MBG** (untuk Lag-time Validator)
- Format: perlu diekstrak manual dari halaman web (tabel Wikipedia atau artikel media) menjadi CSV terstruktur dengan kolom: `date`, `sppg_name`, `location`, `region`, `victim_count`, `source`.
- Ini adalah tugas ETL ringan untuk Lead Data Engineer — bukan dataset yang sudah dalam format CSV siap pakai.

---

## 8. Struktur Folder & Pembagian Kerja

Struktur folder mengikuti repo yang sudah ada: `nutriwatch-indonesia-alert/`. Setiap folder berikut sudah ada sebagai placeholder dan diisi sesuai rincian di bawah.

### 8.1 `data-engineering/` — Lead Data Engineer

```
data-engineering/
├── kafka/
│   ├── producer.py          # Replay dataset teks MBG ke topic Kafka "mbg-text-stream"
│   └── config.yaml          # Konfigurasi topic, broker, rate replay
├── nifi/
│   ├── ingest_incidents.xml # NiFi flow template: ETL data insiden resmi (web → CSV → HDFS)
│   └── incidents_schema.csv # Skema kolom: date, sppg_name, location, region, victim_count, source
└── README.md                # Cara menjalankan producer dan NiFi flow
```

**Deliverable:**
1. Script Kafka Producer yang membaca dataset teks MBG dan mempublikasikan tiap baris sebagai message ke topic `mbg-text-stream`, dengan opsi mengatur kecepatan replay (messages/detik) agar bisa didemonstrasikan dalam waktu wajar.
2. CSV terekstrak dari sumber insiden resmi (Wikipedia/media), divalidasi tidak ada duplikat tanggal+SPPG.
3. NiFi flow (atau script Python sebagai alternatif jika NiFi tidak tersedia) yang memuat CSV insiden tersebut ke HDFS path `/nutriwatch/incidents/raw/`.

### 8.2 `big-data-processing/` — Big Data Developer

```
big-data-processing/
├── spark/
│   ├── streaming_job.py     # Konsumsi topic Kafka, windowing per hari
│   └── feature_extractor.py # Hitung tweet_volume, negative_ratio, dominant_aspect per window
└── README.md
```

**Deliverable:**
1. Spark Structured Streaming job yang mengonsumsi `mbg-text-stream`, menggunakan watermark + tumbling window 1 hari, dikelompokkan per wilayah (default: "Jawa" jika metadata lokasi tidak tersedia per teks).
2. Feature extractor yang menerima hasil klasifikasi ABSA (dari komponen 8.3) dan menghasilkan satu baris fitur window per hari per wilayah, dengan skema:
   ```
   window_date: date
   region: string
   tweet_volume: integer
   negative_ratio: float (0-100)
   dominant_aspect: string (salah satu dari 4 kode aspek di Bagian 5)
   ```
3. Output fitur window disimpan ke HDFS path `/nutriwatch/features/daily/` dalam format Parquet.

### 8.3 `ml-nlp/` — ML & NLP Specialist

```
ml-nlp/
├── absa/
│   └── indobert_absa.py     # Fine-tuned IndoBERT, klasifikasi aspek + sentimen per teks
├── anomaly/
│   └── isolation_forest.py  # Input: fitur window, output: anomaly_score, is_signal
├── validation/
│   └── lag_evaluator.py     # Bandingkan signal_events vs incident_records, hitung lag & match rate
└── README.md
```

**Deliverable:**
1. Model IndoBERT (gunakan base model seperti `indobenchmark/indobert-base-p1` atau `indolem/indobert-base-uncased`, fine-tuned jika ada waktu, atau zero-shot/few-shot prompting jika tidak ada waktu fine-tuning) yang menerima satu teks dan mengembalikan:
   ```
   aspect: string (salah satu dari 4 kode aspek)
   sentiment: string ("positive" | "negative" | "neutral")
   confidence: float (0-1)
   ```
2. Model Isolation Forest (scikit-learn `IsolationForest`) dilatih dari data fitur window historis (kolom `tweet_volume`, `negative_ratio`, representasi numerik `dominant_aspect` via one-hot encoding). Parameter `contamination` disarankan dimulai dari 0.05–0.1 (asumsi 5-10% window dianggap anomali), bisa disesuaikan setelah eksplorasi data. Output per window:
   ```
   window_date: date
   region: string
   anomaly_score: float (0-1)
   is_signal: boolean
   ```
3. Script validasi (`lag_evaluator.py`) yang mengimplementasikan logika di Bagian 5 ("Validasi lag-time") — untuk setiap `is_signal=true`, cari insiden resmi dalam rentang `[d, d+7]` di Wilayah II, hitung `lag_days`, dan hasilkan tabel ringkasan:
   ```
   total_signals: integer
   total_incidents: integer
   matched_incidents: integer
   match_rate_pct: float
   avg_lag_days: float (rata-rata dari yang matched saja)
   median_lag_days: float
   ```

### 8.4 `database-storage/` — Database & Storage Engineer

```
database-storage/
├── hdfs/
│   ├── schema_raw_text.md       # Skema path dan partisi untuk raw text log
│   ├── schema_features.md       # Skema path Parquet fitur window
│   └── schema_incidents.md      # Skema path data insiden resmi
├── elasticsearch/
│   ├── index_signal_events.json    # Index mapping untuk signal_events
│   ├── index_validation.json       # Index mapping untuk validation_results
│   └── query_examples.md           # Contoh query untuk dashboard (per wilayah, per tanggal, dst.)
└── README.md
```

**Deliverable:**
1. Struktur partisi HDFS yang jelas, contoh: `/nutriwatch/raw_text/year=2025/month=09/day=22/`, `/nutriwatch/features/daily/year=2025/month=09/`, `/nutriwatch/incidents/raw/`.
2. Index mapping Elasticsearch untuk dua index utama:
   - `signal_events`: berisi semua window dengan field `window_date`, `region`, `anomaly_score`, `is_signal`, `tweet_volume`, `negative_ratio`, `dominant_aspect`.
   - `validation_results`: berisi hasil dari `lag_evaluator.py`, field `signal_date`, `matched_incident_id`, `lag_days`, `matched` (boolean).
3. Endpoint/query API (bisa pakai Elasticsearch langsung via REST, atau wrapper Flask sederhana) yang dipanggil dashboard React — lihat kontrak API di Bagian 9.

### 8.5 `frontend/` — UI/UX & Frontend Developer

Tidak dirinci di PRD ini karena akan diberikan terpisah sebagai prompt khusus untuk Lovable AI. Frontend developer (atau Lovable) WAJIB mengikuti kontrak API di Bagian 9 agar bisa diintegrasikan tanpa perubahan besar saat backend selesai.

---

## 9. Kontrak API untuk Frontend

Backend (siapa pun yang mengimplementasikan endpoint, baik via Flask wrapper atau langsung query Elasticsearch) harus mengembalikan data sesuai struktur berikut. Frontend harus dibangun mengasumsikan struktur data ini.

```typescript
export interface SignalEvent {
  id: string;
  window_date: string;        // ISO date, format YYYY-MM-DD
  region: string;              // contoh: "Jawa"
  anomaly_score: number;       // 0.0 - 1.0
  is_signal: boolean;
  tweet_volume: number;
  negative_ratio: number;      // 0 - 100
  dominant_aspect: "rasa_menu" | "porsi_kecukupan" | "distribusi_ketepatan" | "higienitas_keamanan";
}

export interface AspectBreakdown {
  aspect: "rasa_menu" | "porsi_kecukupan" | "distribusi_ketepatan" | "higienitas_keamanan";
  negative_pct: number;         // 0 - 100
  total_mentions: number;
  window_date: string;
}

export interface IncidentRecord {
  id: string;
  date: string;                 // ISO date
  sppg_name: string;
  location: string;
  region: string;
  victim_count: number;
  source: "BGN" | "JPPI" | "Wikipedia";
}

export interface ValidationResult {
  signal_id: string;
  matched_incident_id: string | null;
  lag_days: number | null;      // positif = sinyal mendahului insiden
  matched: boolean;
}

export interface RegionSummaryStats {
  region: string;
  total_texts_processed: number;
  total_signals_detected: number;     // dalam periode tertentu, misal 30 hari terakhir
  total_incidents_recorded: number;
  match_rate_pct: number;
  avg_lag_days: number | null;
  median_lag_days: number | null;
  last_updated: string;                // ISO timestamp
}

export interface PipelineStatus {
  kafka_topics: { name: string; msg_per_min: number; lag: number }[];
  spark_throughput_rps: number;
  model_versions: { name: string; version: string }[];
  stream_healthy: boolean;
}
```

Endpoint yang disarankan (REST, bisa disesuaikan implementasinya):
- `GET /api/signals?days=30` → `SignalEvent[]`
- `GET /api/aspects?days=30` → `AspectBreakdown[]`
- `GET /api/incidents?days=30` → `IncidentRecord[]`
- `GET /api/validation?days=30` → `ValidationResult[]`
- `GET /api/stats` → `RegionSummaryStats`
- `GET /api/pipeline-status` → `PipelineStatus`

---

## 10. Kriteria Evaluasi & Definition of Done

| Komponen | Definition of Done |
|---|---|
| Kafka Producer | Bisa mereplay minimal 1000 baris dataset teks dengan rate yang bisa diatur, dan konsumen lain bisa membaca dari topic tersebut |
| NiFi/ETL Insiden | CSV insiden resmi tervalidasi (tidak ada duplikat, semua kolom wajib terisi), berhasil masuk ke HDFS |
| Spark Streaming | Menghasilkan minimal 1 baris fitur window per hari per wilayah dari data yang di-replay, tanpa data loss |
| IndoBERT ABSA | Akurasi klasifikasi aspek minimal diuji manual pada sample (tidak perlu benchmark formal jika waktu terbatas, tapi harus didokumentasikan contoh hasil klasifikasi) |
| Isolation Forest | Model berhasil menghasilkan anomaly_score yang terdistribusi wajar (tidak semua window dianggap sinyal, tidak semua dianggap normal) |
| Lag Evaluator | Menghasilkan match_rate_pct dan avg_lag_days yang terdokumentasi, apa pun hasilnya (tinggi atau rendah — yang penting metodologinya benar) |
| Elasticsearch | Kedua index (signal_events, validation_results) bisa di-query dan mengembalikan data sesuai skema |
| Dashboard | Menampilkan semua field dari kontrak API di Bagian 9 tanpa data hardcoded saat backend sudah siap |

---

## 11. Batasan & Asumsi Penting

1. Sistem ini adalah prototipe akademik, bukan sistem produksi yang dipakai otoritas sungguhan.
2. Hasil match_rate_pct yang rendah BUKAN berarti proyek gagal — itu adalah temuan riset yang valid dan harus dilaporkan jujur di laporan akhir.
3. Resolusi lokasi terbatas pada level wilayah (Jawa), bukan per kabupaten/kota, kecuali dataset teks ternyata punya metadata lokasi yang cukup baik untuk breakdown lebih detail (opsional, bukan wajib).
4. Tidak ada klaim bahwa sistem ini bisa dipakai untuk mencegah insiden secara langsung — sistem ini adalah alat analisis dan eksplorasi data, bukan sistem operasional pencegahan.

---

## Lampiran: Glosarium

- **ABSA (Aspect-Based Sentiment Analysis)**: teknik NLP yang mengklasifikasikan sentimen per aspek spesifik dalam satu teks, bukan sentimen umum keseluruhan teks.
- **Isolation Forest**: algoritma machine learning unsupervised untuk deteksi anomali, bekerja dengan mengisolasi titik data melalui partisi acak berulang — titik yang lebih cepat terisolasi dianggap lebih anomali.
- **Window**: satuan waktu agregasi data, dalam proyek ini didefinisikan sebagai 1 hari.
- **Lag time**: selisih waktu antara kemunculan sinyal dini dan tanggal insiden resmi tercatat.
- **Replay**: teknik memutar ulang dataset statis melalui sistem streaming (Kafka) untuk simulasi, bukan data live sungguhan.
- **Wilayah Pemantauan BGN**: pembagian administratif resmi BGN untuk memantau MBG — Wilayah I (Sumatra), Wilayah II (Jawa), Wilayah III (Indonesia bagian timur). Proyek ini fokus pada Wilayah II.
