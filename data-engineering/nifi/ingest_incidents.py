import pandas as pd
import os
import subprocess
from datetime import datetime

HDFS_RAW_PATH = "/nutriwatch/incidents/raw"
LOCAL_INCIDENTS_FILE = "incidents_full.csv"

def run_cmd(cmd):
    """Run shell command and return output."""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command failed: {cmd}\nError: {err}")
    return out

def main():
    print("=" * 80)
    print("NUTRIWATCH: Ingest Incident Records to HDFS")
    print("=" * 80)
    
    # 1. Verify local file
    print(f"\n[1] Verifying local file: {LOCAL_INCIDENTS_FILE}")
    if not os.path.exists(LOCAL_INCIDENTS_FILE):
        print(f"    ❌ File not found. Run extract_incidents_from_pdf.py first.")
        return
        
    df = pd.read_csv(LOCAL_INCIDENTS_FILE)
    print(f"    ✓ Loaded {len(df)} records")
    
    # Validation checks
    missing_dates = df['date'].isnull().sum()
    missing_locations = df['location'].isnull().sum()
    
    if missing_dates > 0 or missing_locations > 0:
        print(f"    ❌ Validation failed: {missing_dates} missing dates, {missing_locations} missing locations")
        return
        
    print("    ✓ Data validation passed")
    
    # 2. Check HDFS availability
    print(f"\n[2] Checking HDFS via Docker (container: nutriwatch-namenode)")
    try:
        run_cmd("docker exec nutriwatch-namenode hdfs dfs -ls /")
        print("    ✓ HDFS is accessible")
    except Exception as e:
        print("    ❌ Failed to access HDFS. Is the container running?")
        print(f"       Error: {str(e)[:100]}...")
        return
        
    # 3. Create HDFS directory
    print(f"\n[3] Creating HDFS directory: {HDFS_RAW_PATH}")
    try:
        run_cmd(f"docker exec nutriwatch-namenode hdfs dfs -mkdir -p {HDFS_RAW_PATH}")
        print("    ✓ Directory created/exists")
    except Exception as e:
        print(f"    ❌ Failed to create directory: {e}")
        return
        
    # 4. Upload file
    # For Docker, we first need to copy the file into the container, then put to HDFS
    print(f"\n[4] Uploading {LOCAL_INCIDENTS_FILE} to HDFS...")
    try:
        # Step A: Copy from host to container
        print("    ... copying to namenode container")
        run_cmd(f"docker cp {LOCAL_INCIDENTS_FILE} nutriwatch-namenode:/tmp/{LOCAL_INCIDENTS_FILE}")
        
        # Step B: Put from container local to HDFS
        print(f"    ... putting to HDFS {HDFS_RAW_PATH}/{LOCAL_INCIDENTS_FILE}")
        run_cmd(f"docker exec nutriwatch-namenode hdfs dfs -put -f /tmp/{LOCAL_INCIDENTS_FILE} {HDFS_RAW_PATH}/{LOCAL_INCIDENTS_FILE}")
        
        # Step C: Clean up container temp file
        run_cmd(f"docker exec nutriwatch-namenode rm /tmp/{LOCAL_INCIDENTS_FILE}")
        
        print("    ✓ Upload completed successfully")
    except Exception as e:
        print(f"    ❌ Upload failed: {e}")
        return
        
    # 5. Verify upload
    print(f"\n[5] Verifying HDFS contents")
    try:
        ls_out = run_cmd(f"docker exec nutriwatch-namenode hdfs dfs -ls {HDFS_RAW_PATH}")
        print("    Current contents:")
        for line in ls_out.split('\n'):
            if line.strip():
                print(f"      {line}")
    except Exception as e:
        print(f"    ⚠️ Verification failed, but upload might have succeeded: {e}")
        
    print("\n" + "=" * 80)
    print("INGESTION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
