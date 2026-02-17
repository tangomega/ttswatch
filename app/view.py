from db import get_recent_snapshots

rows = get_recent_snapshots(20)

print("\n--- Last Snapshots ---")

for row in rows:
    ts, cpu, mem = row
    print(f"{ts} | CPU: {cpu}% | MEM: {mem}%")
