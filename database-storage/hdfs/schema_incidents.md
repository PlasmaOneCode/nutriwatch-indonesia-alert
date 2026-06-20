# HDFS Schema: Incident Records (CSV)

## Path Structure

```
/nutriwatch/incidents/raw/
```

## File Format

CSV (`.csv`), single file, batch uploaded.

## Schema

| Field | Type | Nullable | Description | Example |
|-------|------|----------|-------------|---------|
| `date` | date (YYYY-MM-DD) | No | Tanggal kejadian insiden | `2025-09-22` |
| `sppg_name` | string | Yes | Nama SPPG/dapur | `"SPPG Al Bayyinah"` |
| `location` | string | No | Lokasi insiden (kab/kota + sekolah) | `"Kabupaten Garut - SDN 2 Mandalasari"` |
| `region` | string | No | Provinsi | `"Jawa Barat"` |
| `victim_count` | integer | No | Jumlah korban | `657` |
| `source` | string | No | Sumber data | `"Wikipedia"` |
| `notes` | string | Yes | Catatan tambahan | `"Ditetapkan sebagai KLB"` |

### Catatan

- `source` bernilai salah satu dari: `"Wikipedia"`, `"Tempo"`, `"Kompas (rekap BGN)"`.
- File di-generate dari script `extract_incidents_from_pdf.py`.
- Data ini **HANYA** dipakai untuk validasi lag-time, **BUKAN** sebagai input sinyal dini.

## Contoh Path

```
/nutriwatch/incidents/raw/incidents_full.csv
/nutriwatch/incidents/raw/incidents_wilayah_ii.csv
```
