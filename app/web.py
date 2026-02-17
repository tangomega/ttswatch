from flask import Flask
from db import get_recent_snapshots, get_device_status

app = Flask(__name__)

@app.route("/")
def index():
    snapshots = get_recent_snapshots(20)
    device = get_device_status()

    html = "<h1>TTSWatch Dashboard</h1>"

    if device:
        html += f"""
        <h2>Device Info</h2>
        <p>Name: {device['name']}</p>
        <p>Model: {device['model']}</p>
        <p>Version: {device['version']}</p>
        <p>Serial: {device['serial']}</p>
        """

    html += "<h2>Recent Snapshots</h2><table border='1'>"
    html += "<tr><th>Time</th><th>CPU %</th><th>Mem %</th></tr>"

    for row in snapshots:
        html += f"<tr><td>{row['timestamp']}</td><td>{row['cpu_percent']}</td><td>{row['memory_percent']}</td></tr>"

    html += "</table>"

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
