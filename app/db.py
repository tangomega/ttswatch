import sqlite3

conn = sqlite3.connect("data/ttswatch.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY,
    hostname TEXT,
    version TEXT,
    build TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
