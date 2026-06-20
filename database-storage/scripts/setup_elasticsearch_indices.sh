#!/bin/bash
# =========================================================================
# NutriWatch - Setup Index Elasticsearch
# Tugas: Daniswara Fausta Novanto - Database & Storage Engineer
#
# Membuat ILM policy + index dashboard (alerts, sentiment, risk-zones, stats)
# beserta mapping-nya. Jalankan setelah Elasticsearch container "healthy":
#   bash scripts/setup_elasticsearch_indices.sh
# =========================================================================

set -e

ES_HOST="http://localhost:9200"
MAPPING_DIR="$(dirname "$0")/../elasticsearch/mappings"
ILM_DIR="$(dirname "$0")/../elasticsearch/ilm"

echo ">> Menunggu Elasticsearch siap..."
until curl -s "$ES_HOST/_cluster/health" | grep -q '"status":"green"\|"status":"yellow"'; do
  sleep 2
done
echo ">> Elasticsearch siap."

# -------------------------------------------------------------------
# 1. ILM Policy untuk index alerts
# -------------------------------------------------------------------
echo ">> Membuat ILM policy: nutriwatch-alerts-ilm-policy"
curl -s -X PUT "$ES_HOST/_ilm/policy/nutriwatch-alerts-ilm-policy" \
  -H "Content-Type: application/json" \
  -d @"$ILM_DIR/nutriwatch-alerts-ilm-policy.json" | sed 's/_comment[^,]*,//' > /dev/null

# Hapus field _comment sebelum dikirim (ES tidak mengenal key tersebut)
python3 - "$ILM_DIR/nutriwatch-alerts-ilm-policy.json" "$ES_HOST" <<'EOF'
import json, sys, urllib.request
path, host = sys.argv[1], sys.argv[2]
data = json.load(open(path))
data.pop("_comment", None)
req = urllib.request.Request(
    f"{host}/_ilm/policy/nutriwatch-alerts-ilm-policy",
    data=json.dumps(data).encode(),
    headers={"Content-Type": "application/json"},
    method="PUT",
)
print(urllib.request.urlopen(req).read().decode())
EOF

# -------------------------------------------------------------------
# 2. Index dashboard + mapping
# -------------------------------------------------------------------
create_index() {
  local index_name=$1
  local mapping_file=$2
  echo ">> Membuat index: $index_name"
  python3 - "$mapping_file" "$ES_HOST" "$index_name" <<'EOF'
import json, sys, urllib.request, urllib.error
path, host, index = sys.argv[1], sys.argv[2], sys.argv[3]
data = json.load(open(path))
data.pop("_comment", None)
req = urllib.request.Request(
    f"{host}/{index}",
    data=json.dumps(data).encode(),
    headers={"Content-Type": "application/json"},
    method="PUT",
)
try:
    print(urllib.request.urlopen(req).read().decode())
except urllib.error.HTTPError as e:
    body = e.read().decode()
    if "resource_already_exists_exception" in body:
        print(f"Index {index} sudah ada, dilewati.")
    else:
        raise
EOF
}

# Index alerts dibuat sebagai write alias (rollover) sesuai ILM
echo ">> Membuat index awal untuk alias rollover: nutriwatch-alerts-000001"
create_index "nutriwatch-alerts-000001" "$MAPPING_DIR/nutriwatch-alerts.json"

create_index "nutriwatch-sentiment"   "$MAPPING_DIR/nutriwatch-sentiment.json"
create_index "nutriwatch-risk-zones"  "$MAPPING_DIR/nutriwatch-risk-zones.json"
create_index "nutriwatch-stats"       "$MAPPING_DIR/nutriwatch-stats.json"

echo ">> Selesai. Daftar index saat ini:"
curl -s "$ES_HOST/_cat/indices?v"
