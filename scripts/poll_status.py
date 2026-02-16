import sqlite3
import os
import requests
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings()
load_dotenv()

FGT_IP = os.getenv("FGT_IP")
API_KEY = os.getenv("FGT_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

BASE_URL = f"https://{FGT_IP}/api/v2/monitor"

def save_status(hostname, model, firmware, serial):
    conn = sqlite3.connect("../ttswatch.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO device_status (hostname, model, firmware, serial)
        VALUES (?, ?, ?, ?)
    """, (hostname, model, firmware, serial))

    conn.commit()
    conn.close()

def get_system_status():
    url = f"{BASE_URL}/system/status"
    r = requests.get(url, headers=HEADERS, verify=False)
    data = r.json()

    hostname = data["results"]["hostname"]
    model = data["results"]["model"]
    firmware = data["version"]
    serial = data["serial"]

    if r.status_code == 429:
    print("Rate limited. Sleeping 60 seconds.")
    time.sleep(60)
    return None

    print("\n--- SYSTEM STATUS ---")
    print(hostname, model, firmware)

    save_status(hostname, model, firmware, serial)

def get_license_status():
    url = f"{BASE_URL}/license/status"
    r = requests.get(url, headers=HEADERS, verify=False)
    print("\n--- LICENSE STATUS ---")
    print(r.json())


def get_firmware_info():
    url = f"{BASE_URL}/system/firmware"
    r = requests.get(url, headers=HEADERS, verify=False)
    print("\n--- FIRMWARE INFO ---")
    print(r.json())


get_system_status()
get_license_status()
get_firmware_info()
