import sqlite3
import os
from datetime import datetime, timedelta

# Absolute path to database (one level above /app)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "ttswatch.db")

def cleanup_old_snapshots(days=7):
    """Delete snapshots older than `days` days."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cutoff = datetime.now() - timedelta(days=days)
    cursor.execute("DELETE FROM snapshots WHERE timestamp < ?", (cutoff,))
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Snapshots table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu_percent INTEGER,
            memory_percent INTEGER
        )
    """)

    # Device status table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT,
            model TEXT,
            version TEXT,
            serial TEXT,
            last_updated TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_snapshot(cpu, mem):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO snapshots (timestamp, cpu_percent, memory_percent)
        VALUES (?, ?, ?)
    """, (datetime.utcnow().isoformat(), cpu, mem))

    conn.commit()
    conn.close()


def save_device_status(hostname, model, version, serial):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO device_status (hostname, model, version, serial)
        VALUES (?, ?, ?, ?)
    """, (hostname, model, version, serial.isoformat()))

    conn.commit()
    conn.close()


def get_recent_snapshots(limit=20):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # <-- this makes rows behave like dicts
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM snapshots ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows



def get_device_status():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT hostname, model, version, serial
        FROM device_status
        ORDER BY last_updated DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "hostname": row["hostname"],
            "model": row["model"],
            "version": row["version"],
            "serial": row["serial"]
        }

    return None

def save_device_status(hostname, model, version, serial):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO device_status (hostname, model, version, serial)
        VALUES (?, ?, ?, ?)
    """, (hostname, model, version, serial))

    conn.commit()
    conn.close()

