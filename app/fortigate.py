import requests
from config import FGT_IP, FGT_TOKEN

def get_status():
    url = f"https://{FGT_IP}/api/v2/monitor/system/status"
    headers = {"Authorization": f"Bearer {FGT_TOKEN}"}
    r = requests.get(url, headers=headers, verify=False)

    if r.status_code != 200:
        print("HTTP Error:", r.status_code)
        print(r.text)
        return None

    try:
        return r.json()
    except Exception as e:
        print("JSON Parse Failed:", e)
        print("Response Text:", r.text)
        return None

def get_resources():
    url = f"https://{FGT_IP}/api/v2/monitor/system/resource/usage"
    headers = {"Authorization": f"Bearer {FGT_TOKEN}"}
    r = requests.get(url, headers=headers, verify=False)

    if r.status_code != 200:
        print("Resource Error:", r.status_code)
        return None

    return r.json()
