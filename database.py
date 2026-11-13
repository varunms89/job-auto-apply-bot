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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id SERIAL PRIMARY KEY,
                company VARCHAR(255),
                role_title VARCHAR(255),
                platform VARCHAR(100),
                test_url TEXT,
                deadline_or_time VARCHAR(255),
                prep_topic VARCHAR(100) DEFAULT 'General',
                status VARCHAR(50) DEFAULT 'PENDING',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Create divided views in PostgreSQL
        cursor.execute("""
            CREATE OR REPLACE VIEW submitted_jobs AS
            SELECT id, job_id, platform, title, company, location, url, match_score, match_reasons, status, applied_at, created_at
            FROM jobs
            WHERE status IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED', 'TEST_GIVEN', 'INTERVIEWING', 'OFFERED', 'REJECTED');

            CREATE OR REPLACE VIEW not_submitted_jobs AS
            SELECT id, job_id, platform, title, company, location, url, match_score, match_reasons, status, created_at
            FROM jobs
            WHERE status NOT IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED', 'TEST_GIVEN', 'INTERVIEWING', 'OFFERED', 'REJECTED');
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT,
                role_title TEXT,
                platform TEXT,
                test_url TEXT,
                deadline_or_time TEXT,
                prep_topic TEXT DEFAULT 'General',
                status TEXT DEFAULT 'PENDING',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Create divided views in SQLite
        cursor.execute("DROP VIEW IF EXISTS submitted_jobs;")
        cursor.execute("DROP VIEW IF EXISTS not_submitted_jobs;")
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS submitted_jobs AS
            SELECT id, job_id, platform, title, company, location, url, match_score, match_reasons, status, applied_at, created_at
            FROM jobs
            WHERE status IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED', 'TEST_GIVEN', 'INTERVIEWING', 'OFFERED', 'REJECTED');
        """)
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS not_submitted_jobs AS
            SELECT id, job_id, platform, title, company, location, url, match_score, match_reasons, status, created_at
            FROM jobs
            WHERE status NOT IN ('APPLIED', 'APPLIED_READY', 'SUBMITTED', 'TEST_GIVEN', 'INTERVIEWING', 'OFFERED', 'REJECTED');
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

def update_job_status(identifier: Any, new_status: str):
    """
    Updates the pipeline status of an application (e.g. SUBMITTED, TEST_GIVEN, INTERVIEWING, OFFERED, REJECTED).
    Supports either integer database ID or string job_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    ph = "%s" if DATABASE_URL else "?"
    if str(identifier).isdigit():
        cursor.execute(f"UPDATE jobs SET status = {ph} WHERE id = {ph} OR job_id = {ph}", (new_status, int(identifier), str(identifier)))
    else:
        cursor.execute(f"UPDATE jobs SET status = {ph} WHERE job_id = {ph}", (new_status, str(identifier)))
    conn.commit()
    conn.close()

def get_job_stats() -> Dict[str, int]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, count(*) FROM jobs GROUP BY status")
    stats = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return stats

def record_assessment(company: str, role_title: str, platform: str, test_url: str,
                      deadline_or_time: str, prep_topic: str = "General", status: str = "PENDING", notes: str = "") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    ph = "%s" if DATABASE_URL else "?"
    
    if DATABASE_URL:
        cursor.execute(f"""
            INSERT INTO assessments (company, role_title, platform, test_url, deadline_or_time, prep_topic, status, notes, created_at)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, CURRENT_TIMESTAMP)
            RETURNING id;
        """, (company, role_title, platform, test_url, deadline_or_time, prep_topic, status, notes))
        new_id = cursor.fetchone()[0]
    else:
        cursor.execute(f"""
            INSERT INTO assessments (company, role_title, platform, test_url, deadline_or_time, prep_topic, status, notes, created_at)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, CURRENT_TIMESTAMP);
        """, (company, role_title, platform, test_url, deadline_or_time, prep_topic, status, notes))
        new_id = cursor.lastrowid
        
    conn.commit()
    conn.close()
    return new_id

def get_assessments(status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    ph = "%s" if DATABASE_URL else "?"
    
    if status:
        cursor.execute(f"""
            SELECT id, company, role_title, platform, test_url, deadline_or_time, prep_topic, status, notes, created_at
            FROM assessments
            WHERE status = {ph}
            ORDER BY id DESC
        """, (status,))
    else:
        cursor.execute("""
            SELECT id, company, role_title, platform, test_url, deadline_or_time, prep_topic, status, notes, created_at
            FROM assessments
            ORDER BY CASE WHEN status = 'PENDING' THEN 0 ELSE 1 END, id DESC
        """)
        
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": r[0],
            "company": r[1],
            "role_title": r[2],
            "platform": r[3],
            "test_url": r[4],
            "deadline_or_time": r[5],
            "prep_topic": r[6],
            "status": r[7],
            "notes": r[8],
            "created_at": str(r[9]) if r[9] else ""
        }
        for r in rows
    ]

def update_assessment_status(assessment_id: int, status: str = "COMPLETED"):
    conn = get_connection()
    cursor = conn.cursor()
    ph = "%s" if DATABASE_URL else "?"
    cursor.execute(f"UPDATE assessments SET status = {ph} WHERE id = {ph}", (status, assessment_id))
    conn.commit()
    conn.close()
