# ML & NLP Module — NutriWatch

Modul ini memuat logika analitik dan machine learning untuk proyek NutriWatch.
Terdapat 3 komponen utama:

## 1. IndoBERT Zero-Shot ABSA (`absa/indobert_absa.py`)
Mengekstrak Aspek dan Sentimen dari setiap teks. Karena keterbatasan VRAM (4GB), kita menggunakan pendekatan **Zero-Shot Classification** (`mDeBERTa-v3-base-mnli-xnli`) alih-alih melakukan full fine-tuning pada IndoBERT. 

**Kategori Aspek:**
- `rasa_menu` (Rasa dan menu makanan)
- `porsi_kecukupan` (Porsi dan kecukupan makanan)
- `distribusi_ketepatan` (Distribusi dan ketepatan waktu)
- `higienitas_keamanan` (Higienitas dan keamanan makanan)

**Testing:**
```bash
python absa/indobert_absa.py --test
```

## 2. Isolation Forest Anomaly Detection (`anomaly/isolation_forest.py`)
Model deteksi anomali (unsupervised) untuk mengidentifikasi lonjakan/anomali pada volume keluhan publik.
Model menerima fitur agregasi harian (window feature) dan mengembalikan `anomaly_score` serta label `is_signal`.

**Testing:**
```bash
python anomaly/isolation_forest.py --test
```

## 3. Lag-Time Evaluator (`validation/lag_evaluator.py`)
Melakukan cross-check antara sinyal (anomali) yang dideteksi oleh sistem dengan daftar insiden resmi. Evaluator menghitung metrik seperti *Match Rate* dan rata-rata *Lag Days* (selisih hari antara sinyal dan insiden).

**Testing:**
```bash
python validation/lag_evaluator.py --test
```
