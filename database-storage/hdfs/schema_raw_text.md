# HDFS Schema: Raw Text Log

## Path Structure

```
/nutriwatch/raw_text/year=YYYY/month=MM/day=DD/
```

## Partitioning

- **Level 1**: `year` (e.g., `year=2025`)
- **Level 2**: `month` (e.g., `month=09`)
- **Level 3**: `day` (e.g., `day=22`)

## File Format

JSON Lines (`.jsonl`), satu baris per teks.

## Schema

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `text_id` | string (UUID) | ID unik per teks | `"a1b2c3d4-..."` |
| `text` | string | Isi teks asli (tweet/komentar) | `"Menu MBG hari ini rasanya hambar"` |
| `timestamp` | string (ISO 8601) | Waktu publikasi teks | `"2025-09-22T14:30:00+07:00"` |
| `source` | string | Platform asal | `"twitter"` |
| `region` | string | Wilayah (default "Jawa") | `"Jawa"` |
| `aspect` | string | Hasil klasifikasi ABSA aspek | `"rasa_menu"` |
| `sentiment` | string | Hasil klasifikasi sentimen | `"negative"` |
| `confidence` | float | Confidence score model | `0.87` |

## Contoh Path

```
/nutriwatch/raw_text/year=2025/month=09/day=22/part-00000.jsonl
/nutriwatch/raw_text/year=2025/month=09/day=23/part-00000.jsonl
```

## Retention

Data dipertahankan selama periode analisis (tidak ada TTL untuk prototipe akademik).
