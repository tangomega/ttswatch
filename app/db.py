import sqlite3
import os
from datetime import datetime

# Absolute path to database (one level above /app)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "ttswatch.db")


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
        INSERT INTO device_status (hostname, model, version, serial, last_updated)
        VALUES (?, ?, ?, ?, ?)
    """, (hostname, model, version, serial, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()


def get_recent_snapshots(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, cpu_percent, memory_percent
        FROM snapshots
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows

