from flask import Flask
from db import get_recent_snapshots, get_device_status

app = Flask(__name__)

@app.route("/")
def index():
    # Fetch device info (assumes single device row)
    device = get_device_status()  # returns a dict

    # Fetch recent snapshots (most recent 20)
    rows = get_recent_snapshots(20)  # list of sqlite3.Row

    # Start HTML
    html = "<html><head><title>TTSWatch Dashboard</title></head><body>"
    html += "<h1>TTSWatch Dashboard</h1>"

    # Device Info
    if device:
        html += f"<h2>{device.get('hostname', 'Unknown')} ({device.get('model', '')})</h2>"
        html += f"<p>Version: {device.get('version', '')} | Serial: {device.get('serial', '')}</p>"
    else:
        html += "<p>No device information found.</p>"

    # Snapshot Table
    html += "<h3>Recent Snapshots</h3>"
    html += "<table border='1' cellpadding='5' cellspacing='0'>"
    html += "<tr><th>Timestamp</th><th>CPU %</th><th>Memory %</th></tr>"

    if rows:
        for row in rows:
            html += (
                f"<tr>"
                f"<td>{row['timestamp']}</td>"
                f"<td>{row['cpu_percent']}</td>"
                f"<td>{row['memory_percent']}</td>"
                f"</tr>"
            )
    else:
        html += "<tr><td colspan='3'>No snapshots found.</td></tr>"

    html += "</table>"
    html += "</body></html>"

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

