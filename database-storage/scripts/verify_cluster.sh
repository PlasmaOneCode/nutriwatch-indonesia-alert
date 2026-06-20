#!/bin/bash
# =========================================================================
# NutriWatch - Verifikasi Cluster HDFS & Elasticsearch
# Tugas: Daniswara Fausta Novanto - Database & Storage Engineer
#
# Memverifikasi:
#  1. HDFS NameNode & DataNode aktif (report cluster)
#  2. Elasticsearch cluster health
#  3. Index dashboard tersedia dengan mapping yang benar
#  4. Latensi query contoh ke index nutriwatch-alerts & nutriwatch-risk-zones
# =========================================================================

set -e
ES_HOST="http://localhost:9200"

echo "================================================================"
echo "1. STATUS HDFS CLUSTER"
echo "================================================================"
docker exec nutriwatch-namenode hdfs dfsadmin -report | head -20

echo ""
echo "================================================================"
echo "2. ELASTICSEARCH CLUSTER HEALTH"
echo "================================================================"
curl -s "$ES_HOST/_cluster/health?pretty"

echo ""
echo "================================================================"
echo "3. DAFTAR INDEX & ALIAS"
echo "================================================================"
curl -s "$ES_HOST/_cat/indices?v"
echo ""
curl -s "$ES_HOST/_cat/aliases?v"

echo ""
echo "================================================================"
echo "4. LATENSI QUERY DASHBOARD (target < 200ms)"
echo "================================================================"
echo "-- nutriwatch-alerts (sorted by created_at desc) --"
curl -s -o /dev/null -w "HTTP %{http_code} | total time: %{time_total}s\n" \
  -X GET "$ES_HOST/nutriwatch-alerts/_search" \
  -H "Content-Type: application/json" \
  -d '{"sort":[{"created_at":"desc"}],"size":10}'

echo "-- nutriwatch-risk-zones (geo bounding box untuk peta) --"
curl -s -o /dev/null -w "HTTP %{http_code} | total time: %{time_total}s\n" \
  -X GET "$ES_HOST/nutriwatch-risk-zones/_search" \
  -H "Content-Type: application/json" \
  -d '{
        "query": {
          "geo_bounding_box": {
            "location": {
              "top_left": { "lat": 6, "lon": 95 },
              "bottom_right": { "lat": -11, "lon": 141 }
            }
          }
        }
      }'

echo ""
echo "Verifikasi selesai."
