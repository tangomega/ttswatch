import sqlite3

conn = sqlite3.connect("../ttswatch.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS device_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT,
    model TEXT,
    firmware TEXT,
    serial TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database initialized.")
