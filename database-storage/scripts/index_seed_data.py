#!/usr/bin/env python3
"""
NutriWatch - Indexing Data Demo ke Elasticsearch
Tugas: Daniswara Fausta Novanto - Database & Storage Engineer

Skrip ini melakukan bulk-index data contoh (seed_data.json) ke index
nutriwatch-alerts, nutriwatch-sentiment, nutriwatch-risk-zones, dan
nutriwatch-stats. Berguna untuk:
  - Verifikasi mapping sudah benar
  - Menyediakan data dummy agar dashboard frontend bisa langsung diuji
    sebelum pipeline Spark Streaming (Fachry) & ABSA (Irul) selesai

Cara pakai:
  python3 index_seed_data.py
"""

import json
import urllib.request
import urllib.error
from pathlib import Path

ES_HOST = "http://localhost:9200"
SEED_FILE = Path(__file__).parent / "seed_data.json"


def bulk_index(index_name, docs, id_field=None):
    lines = []
    for doc in docs:
        meta = {"index": {"_index": index_name}}
        if id_field and doc.get(id_field):
            meta["index"]["_id"] = doc[id_field]
        lines.append(json.dumps(meta))
        lines.append(json.dumps(doc))
    payload = ("\n".join(lines) + "\n").encode("utf-8")

    req = urllib.request.Request(
        f"{ES_HOST}/_bulk",
        data=payload,
        headers={"Content-Type": "application/x-ndjson"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read().decode())
        errors = result.get("errors")
        print(f"  -> {len(docs)} dokumen dikirim ke '{index_name}'. errors={errors}")
        if errors:
            for item in result["items"]:
                op = item.get("index", {})
                if op.get("error"):
                    print(f"     ERROR id={op.get('_id')}: {op['error']}")
    except urllib.error.HTTPError as e:
        print(f"  -> HTTP ERROR indexing {index_name}: {e.read().decode()}")


def main():
    data = json.loads(SEED_FILE.read_text())

    print("Indexing nutriwatch-alerts ...")
    # gunakan alias write 'nutriwatch-alerts' (rollover) yang sudah dibuat
    bulk_index("nutriwatch-alerts", data["alerts"], id_field="alert_id")

    print("Indexing nutriwatch-sentiment ...")
    bulk_index("nutriwatch-sentiment", data["sentiment"])

    print("Indexing nutriwatch-risk-zones ...")
    bulk_index("nutriwatch-risk-zones", data["risk_zones"], id_field="zone_id")

    print("Indexing nutriwatch-stats ...")
    bulk_index("nutriwatch-stats", data["stats"], id_field="metric_key")

    print("\nSelesai. Cek hasil dengan:")
    print(f"  curl '{ES_HOST}/nutriwatch-alerts/_search?pretty'")
    print(f"  curl '{ES_HOST}/nutriwatch-risk-zones/_search?pretty'")


if __name__ == "__main__":
    main()
