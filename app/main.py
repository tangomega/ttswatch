import schedule
import time
import urllib3
import os
from dotenv import load_dotenv
from fortigate import get_status, get_resources
from db import save_snapshot

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 30))


def job():
    print("\n--- TTSWatch Snapshot ---")

    try:
        status = get_status()
        resources = get_resources()

        if not status or not resources:
            print("Failed to retrieve data")
            return

        s = status.get("results", {})
        r = resources.get("results", {})

        # ---- CPU / MEMORY EXTRACTION ----
        cpu_data = r.get("cpu") or r.get("cpu_usage")
        mem_data = r.get("mem") or r.get("memory") or r.get("memory_usage")

        cpu_current = None
        mem_current = None

        if isinstance(cpu_data, list) and len(cpu_data) > 0:
            cpu_current = cpu_data[0].get("current")

        if isinstance(mem_data, list) and len(mem_data) > 0:
            mem_current = mem_data[0].get("current")

        # ---- UPTIME EXTRACTION ----
        uptime = (
            s.get("uptime")
            or s.get("system_uptime")
            or s.get("uptime_sec")
        )

        # ---- SNAPSHOT PRINT ----
        print(f"hostname: {s.get('hostname')}")
        print(f"model: {s.get('model')}")
        print(f"version: {status.get('version')}")
        print(f"build: {status.get('build')}")
        print(f"uptime: {uptime if uptime else 'N/A'}")
        print(f"cpu_percent: {cpu_current}")
        print(f"memory_percent: {mem_current}")

        # ---- SAVE TO DATABASE ----
        if cpu_current is not None and mem_current is not None:
            save_snapshot(cpu_current, mem_current)
            print("Snapshot saved to DB")

    except Exception as e:
        print("Job Error:", e)


# ---- SCHEDULER SETUP ----
schedule.every(POLL_INTERVAL).seconds.do(job)

print(f"TTSWatch started. Polling every {POLL_INTERVAL} seconds.")

# Immediate first run
job()

# Infinite loop
while True:
    schedule.run_pending()
    time.sleep(1)

