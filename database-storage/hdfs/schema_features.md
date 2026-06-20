# HDFS Schema: Daily Feature Window (Parquet)

## Path Structure

```
/nutriwatch/features/daily/year=YYYY/month=MM/
```

## Partitioning

- **Level 1**: `year` (e.g., `year=2025`)
- **Level 2**: `month` (e.g., `month=09`)

## File Format

Apache Parquet (`.parquet`), partitioned by year/month.

## Schema

| Field | Type | Nullable | Description | Example |
|-------|------|----------|-------------|---------|
| `window_date` | date | No | Tanggal window (1 hari) | `2025-09-22` |
| `region` | string | No | Wilayah pemantauan | `"Jawa"` |
| `tweet_volume` | integer | No | Jumlah teks dalam window | `142` |
| `negative_ratio` | float | No | Persentase sentimen negatif (0-100) | `45.3` |
| `dominant_aspect` | string | No | Aspek keluhan terbanyak | `"higienitas_keamanan"` |

### Catatan

- `dominant_aspect` bernilai salah satu dari 4 kode aspek:
  - `rasa_menu`
  - `porsi_kecukupan`
  - `distribusi_ketepatan`
  - `higienitas_keamanan`

- `negative_ratio` dihitung sebagai: `(count_negative / total_texts_in_window) * 100`

## Contoh Path

```
/nutriwatch/features/daily/year=2025/month=09/part-00000.parquet
/nutriwatch/features/daily/year=2025/month=10/part-00000.parquet
```
