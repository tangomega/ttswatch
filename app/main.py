import schedule
import urllib3
import time
import os
from dotenv import load_dotenv
from fortigate import get_status, get_resources

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 60))

def job():
    print("\n--- TTSWatch Snapshot ---")
    
    try:
        status = get_status()        # /system/status
        resources = get_resources()  # /system/performance/status

        if not status or not resources:
            print("Failed to retrieve data")
            return

        # System info
        s = status.get("results", {})
        r = resources.get("results", {})

        # Uptime
        uptime_seconds = s.get("uptime")
        if uptime_seconds is not None:
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            seconds = uptime_seconds % 60
            uptime_str = f"{hours}h {minutes}m {seconds}s"
        else:
            uptime_str = "N/A"

        # CPU & memory
        cpu_data = r.get("cpu") or r.get("cpu_usage")
        mem_data = r.get("mem") or r.get("memory") or r.get("memory_usage")

        cpu_current = None
        mem_current = None

        if isinstance(cpu_data, list) and len(cpu_data) > 0:
            cpu_current = cpu_data[0].get("current")

        if isinstance(mem_data, list) and len(mem_data) > 0:
            mem_current = mem_data[0].get("current")

        # Snapshot
        snapshot = {
            "hostname": s.get("hostname"),
            "model": s.get("model"),
            "version": status.get("version"),
            "build": status.get("build"),
            "uptime": uptime_str,
            "cpu_percent": cpu_current,
            "memory_percent": mem_current,
        }

        # Print snapshot
        for key, value in snapshot.items():
            print(f"{key}: {value}")

    except Exception as e:
        print("Job Error:", e)

# Schedule polling
schedule.every(POLL_INTERVAL).seconds.do(job)

print(f"TTSWatch started. Polling every {POLL_INTERVAL} seconds.")

# Optional immediate first run
job()

while True:
    schedule.run_pending()
    time.sleep(1)

