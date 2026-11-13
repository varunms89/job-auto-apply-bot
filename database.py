import os
import sqlite3
from typing import Optional, List, Dict, Any

# Checks for DATABASE_URL environment variable or local .env
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # Auto-load from .env if present
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("DATABASE_URL="):
                    DATABASE_URL = line.split("=", 1)[1].strip()
                    break

# Local fallback to SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "jobs_bot.db")

def get_connection():
    if DATABASE_URL:
        import psycopg2
        return psycopg2.connect(DATABASE_URL)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    if DATABASE_URL:
        # PostgreSQL schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                job_id VARCHAR(255) UNIQUE,
                platform VARCHAR(100),
                title VARCHAR(255),
                company VARCHAR(255),
                location VARCHAR(255),
                url TEXT,
                description TEXT,
                match_score REAL,
                match_reasons TEXT,
                status VARCHAR(50) DEFAULT 'DISCOVERED',
                applied_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS govt_notifications (
                id SERIAL PRIMARY KEY,
                portal VARCHAR(100),
                notification_title TEXT,
                post_name VARCHAR(255),
                qualification VARCHAR(255),
                last_date VARCHAR(100),
                link TEXT UNIQUE,
                status VARCHAR(50) DEFAULT 'NEW',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Create divided views in PostgreSQL
        cursor.execute("""
            CREATE OR REPLACE VIEW submitted_jobs AS
            SELECT id, job_id, platform, title, company, location, url, match_score, match_reasons, status, applied_at, created_at
            FROM jobs
            WHERE status IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED');

            CREATE OR REPLACE VIEW not_submitted_jobs AS
            SELECT id, job_id, platform, title, company, location, url, match_score, match_reasons, status, created_at
            FROM jobs
            WHERE status NOT IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED');
        """)
    else:
        # SQLite schema
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
                status TEXT DEFAULT 'DISCOVERED',
                applied_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS govt_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portal TEXT,
                notification_title TEXT,
                post_name TEXT,
                qualification TEXT,
                last_date TEXT,
                link TEXT UNIQUE,
                status TEXT DEFAULT 'NEW',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Create divided views in SQLite
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS submitted_jobs AS
            SELECT id, job_id, platform, title, company, location, url, match_score, match_reasons, status, applied_at, created_at
            FROM jobs
            WHERE status IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED');
        """)
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS not_submitted_jobs AS
            SELECT id, job_id, platform, title, company, location, url, match_score, match_reasons, status, created_at
            FROM jobs
            WHERE status NOT IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED');
        """)
    conn.commit()
    conn.close()

def is_job_applied_or_seen(job_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    ph = "%s" if DATABASE_URL else "?"
    cursor.execute(f"SELECT status FROM jobs WHERE job_id = {ph}", (job_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def record_job(job_id: str, platform: str, title: str, company: str, location: str, url: str, 
               description: str = "", match_score: float = 0.0, match_reasons: str = "", status: str = "DISCOVERED"):
    conn = get_connection()
    cursor = conn.cursor()
    
    if DATABASE_URL:
        # PostgreSQL ON CONFLICT DO UPDATE
        cursor.execute("""
            INSERT INTO jobs 
            (job_id, platform, title, company, location, url, description, match_score, match_reasons, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (job_id) DO UPDATE SET
                title = EXCLUDED.title,
                match_score = EXCLUDED.match_score,
                match_reasons = EXCLUDED.match_reasons,
                status = EXCLUDED.status;
        """, (job_id, platform, title, company, location, url, description, match_score, match_reasons, status))
    else:
        # SQLite INSERT OR REPLACE
        cursor.execute("""
            INSERT OR REPLACE INTO jobs 
            (job_id, platform, title, company, location, url, description, match_score, match_reasons, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (job_id, platform, title, company, location, url, description, match_score, match_reasons, status))
        
    conn.commit()
    conn.close()

def mark_applied(job_id: str, status: str = "APPLIED"):
    conn = get_connection()
    cursor = conn.cursor()
    ph = "%s" if DATABASE_URL else "?"
    cursor.execute(f"""
        UPDATE jobs 
        SET status = {ph}, applied_at = CURRENT_TIMESTAMP 
        WHERE job_id = {ph}
    """, (status, job_id))
    conn.commit()
    conn.close()

def get_job_stats() -> Dict[str, int]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, count(*) FROM jobs GROUP BY status")
    stats = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return stats
