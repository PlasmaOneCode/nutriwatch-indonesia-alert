#!/bin/bash
# =========================================================================
# NutriWatch - Setup Direktori HDFS (Cold Storage)
# Tugas: Daniswara Fausta Novanto - Database & Storage Engineer
#
# Membuat struktur direktori HDFS untuk:
#  - Landing zone (data mentah dari NiFi/Kafka)
#  - Processed zone (output Spark Streaming)
#  - Dataset training model (ML & NLP)
#
# Jalankan setelah cluster HDFS (namenode + datanode) berjalan:
#   bash scripts/setup_hdfs_dirs.sh
# =========================================================================

set -e

NAMENODE_CONTAINER="nutriwatch-namenode"

echo ">> Menunggu NameNode keluar dari safemode..."
docker exec $NAMENODE_CONTAINER hdfs dfsadmin -safemode wait

echo ">> Membuat struktur direktori HDFS untuk NutriWatch..."

# Landing zone - data mentah dari Apache NiFi (per topik Kafka)
docker exec $NAMENODE_CONTAINER hdfs dfs -mkdir -p /nutriwatch/landing/dapur-umum-events
docker exec $NAMENODE_CONTAINER hdfs dfs -mkdir -p /nutriwatch/landing/keluhan-stream
docker exec $NAMENODE_CONTAINER hdfs dfs -mkdir -p /nutriwatch/landing/anggaran-events

# Processed zone - hasil agregasi & join Spark Streaming
docker exec $NAMENODE_CONTAINER hdfs dfs -mkdir -p /nutriwatch/processed/alerts
docker exec $NAMENODE_CONTAINER hdfs dfs -mkdir -p /nutriwatch/processed/sentiment_absa
docker exec $NAMENODE_CONTAINER hdfs dfs -mkdir -p /nutriwatch/processed/risk_zones

# Dataset training - ML & NLP (IndoBERT, Isolation Forest)
docker exec $NAMENODE_CONTAINER hdfs dfs -mkdir -p /nutriwatch/datasets/indobert_absa
docker exec $NAMENODE_CONTAINER hdfs dfs -mkdir -p /nutriwatch/datasets/isolation_forest

# Set replication factor sesuai konfigurasi (2x)
docker exec $NAMENODE_CONTAINER hdfs dfs -setrep -R 2 /nutriwatch

echo ">> Struktur direktori HDFS berhasil dibuat:"
docker exec $NAMENODE_CONTAINER hdfs dfs -ls -R /nutriwatch
