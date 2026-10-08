import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), "jobs_bot.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT UNIQUE,
            platform TEXT,
            title TEXT,
            company TEXT,
            location TEXT,
            url TEXT,
            description TEXT,
            match_score REAL,
            match_reasons TEXT,
            status TEXT DEFAULT 'DISCOVERED', -- DISCOVERED, APPLIED, SKIPPED, FAILED
            applied_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS govt_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portal TEXT, -- KPSC, KEA, RRB
            notification_title TEXT,
            post_name TEXT,
            qualification TEXT,
            last_date TEXT,
            link TEXT UNIQUE,
            status TEXT DEFAULT 'NEW',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_job_applied_or_seen(job_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM jobs WHERE job_id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def record_job(job_id: str, platform: str, title: str, company: str, location: str, url: str, 
               description: str = "", match_score: float = 0.0, match_reasons: str = "", status: str = "DISCOVERED"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO jobs 
        (job_id, platform, title, company, location, url, description, match_score, match_reasons, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (job_id, platform, title, company, location, url, description, match_score, match_reasons, status))
    conn.commit()
    conn.close()

def mark_applied(job_id: str, status: str = "APPLIED"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE jobs 
        SET status = ?, applied_at = CURRENT_TIMESTAMP 
        WHERE job_id = ?
    """, (status, job_id))
    conn.commit()
    conn.close()

def get_job_stats() -> Dict[str, int]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status, count(*) FROM jobs GROUP BY status")
    stats = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return stats
