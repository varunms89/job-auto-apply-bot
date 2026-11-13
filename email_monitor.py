import os
import re
import imaplib
import email
from email.header import decode_header
from typing import Dict, Optional, List, Any
from urllib.parse import urlparse

from database import record_assessment, get_assessments
from telegram_notifier import send_assessment_alert

KNOWN_PLATFORMS = {
    "hackerrank.com": "HackerRank",
    "codility.com": "Codility",
    "testgorilla.com": "TestGorilla",
    "mettl.com": "Mercer Mettl",
    "hirevue.com": "HireVue",
    "hackerearth.com": "HackerEarth",
    "elitmus.com": "eLitmus",
    "myamcat.com": "AMCAT",
    "joinsuperset.com": "Superset",
    "unstop.com": "Unstop",
    "meet.google.com": "Google Meet (Interview)",
    "zoom.us": "Zoom (Interview)",
    "teams.microsoft.com": "MS Teams (Interview)",
    "teams.live.com": "MS Teams (Interview)",
    "webex.com": "Cisco Webex"
}

ASSESSMENT_KEYWORDS = [
    "online assessment", "coding test", "take test", "assessment link",
    "coding challenge", "technical assessment", "hiring test",
    "interview invitation", "schedule your interview", "video interview",
    "technical interview", "online test invitation", "test window", "test deadline"
]

def clean_header_text(header_val: str) -> str:
    if not header_val:
        return ""
    decoded_parts = decode_header(header_val)
    result = []
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="ignore"))
        else:
            result.append(str(part))
    return "".join(result).strip()

def extract_platform_and_link(body: str) -> tuple:
    """
    Extracts test / interview link and identifies the platform.
    """
    url_pattern = r'https?://[^\s<>"\')]+'
    urls = re.findall(url_pattern, body)
    
    # Check for known platforms first
    for u in urls:
        parsed = urlparse(u)
        hostname = parsed.hostname.lower() if parsed.hostname else ""
        for domain, name in KNOWN_PLATFORMS.items():
            if domain in hostname:
                return name, u

    # Check for generic test / interview URLs
    for u in urls:
        u_lower = u.lower()
        if any(k in u_lower for k in ["assessment", "test", "candidate", "interview", "challenge", "screening"]):
            return "Company Assessment Portal", u

    return None, None

def extract_deadline_or_time(text: str) -> str:
    """
    Attempts to parse deadline or interview time from text.
    """
    patterns = [
        r'(?:deadline|valid until|expires on|complete before|submit by|due by)[:\s]+([^\n\.,]+)',
        r'(?:scheduled on|date & time|timing)[:\s]+([^\n\.,]+)',
        r'(?:before|by)[:\s]+([A-Za-z]{3,9}\s+\d{1,2}(?:,\s*\d{4})?)',
        r'(?:within|in)\s+(\d+\s+(?:hours?|days?))'
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return "Complete as soon as possible (usually 48 hrs)"

def classify_topic(text: str) -> str:
    """
    Determines whether the role/test is QA, Python, AI, or General.
    """
    t_lower = text.lower()
    if any(k in t_lower for k in ["qa", "tester", "testing", "quality assurance", "selenium", "manual"]):
        return "Software Testing / QA"
    elif any(k in t_lower for k in ["ai", "machine learning", "ml", "artificial intelligence", "data science"]):
        return "AI & Machine Learning"
    elif any(k in t_lower for k in ["python", "developer", "coding", "software engineer", "backend", "full stack"]):
        return "Python & Programming"
    return "General Tech & Aptitude"

def extract_company_name(subject: str, sender: str, body: str) -> str:
    """
    Infers company name from email subject, sender address or body.
    """
    # e.g., "Siemens Online Assessment", "Interview with Amazon"
    m = re.search(r'(?:from|with|at)\s+([A-Z][a-zA-Z0-9\s&]+?)(?:\s+-\s+|\s+online|\s+assessment|\s+interview|$)', subject, re.IGNORECASE)
    if m:
        comp = m.group(1).strip()
        if len(comp) > 2 and len(comp) < 30:
            return comp
    
    # Try sender domain
    sender_domain = sender.split("@")[-1].replace(">", "").strip() if "@" in sender else ""
    if sender_domain and not any(common in sender_domain for common in ["gmail.com", "yahoo.com", "outlook.com", "hackerrank.com", "testgorilla.com"]):
        parts = sender_domain.split(".")
        if len(parts) >= 2:
            return parts[0].capitalize()

    return "Hiring Team"

def process_email_message(subject: str, sender: str, body_text: str, auto_alert: bool = True) -> Optional[Dict[str, Any]]:
    """
    Analyzes an email to see if it is a test invitation or interview session.
    If matched, records it to the database and dispatches an instant Telegram alert.
    """
    combined = f"{subject} {body_text}".lower()
    
    # Check for assessment keywords
    is_assessment = any(kw in combined for kw in ASSESSMENT_KEYWORDS)
    platform, test_url = extract_platform_and_link(body_text)

    if not is_assessment and not platform:
        return None

    company = extract_company_name(subject, sender, body_text)
    deadline = extract_deadline_or_time(body_text)
    topic = classify_topic(combined)
    role_title = subject.replace("Online Assessment", "").replace("Invitation", "").strip() or "Candidate Assessment"
    
    if not test_url:
        test_url = "https://mail.google.com"

    # Save to database
    assessment_id = record_assessment(
        company=company,
        role_title=role_title,
        platform=platform or "Assessment Portal",
        test_url=test_url,
        deadline_or_time=deadline,
        prep_topic=topic,
        status="PENDING",
        notes=f"Detected from email subject: {subject}"
    )

    result = {
        "id": assessment_id,
        "company": company,
        "role_title": role_title,
        "platform": platform or "Assessment Portal",
        "test_url": test_url,
        "deadline_or_time": deadline,
        "prep_topic": topic
    }

    # Dispatch High Priority Telegram Alert
    if auto_alert:
        send_assessment_alert(
            company=company,
            role_title=role_title,
            platform=platform or "Assessment Portal",
            test_url=test_url,
            deadline_or_time=deadline,
            prep_topic=topic,
            instructions=f"Received via email ({sender}). Review practice questions before opening the test link!"
        )

    return result

def load_env_credentials():
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().replace('"', '').replace("'", '')
                    if k not in os.environ:
                        os.environ[k] = v

def check_gmail_inbox() -> int:
    """
    Connects to Gmail via IMAP if credentials exist in environment or .env.
    Scans recent unseen messages specifically for assessment & interview invitations.
    """
    load_env_credentials()
    user = os.environ.get("IMAP_USER") or os.environ.get("EMAIL_USER")
    password = os.environ.get("IMAP_PASSWORD") or os.environ.get("EMAIL_PASSWORD")

    if not user or not password:
        return 0

    password = password.replace(" ", "")
    detected_count = 0
    try:
        from datetime import datetime, timedelta
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user, password)
        mail.select("inbox")

        # Inspect unread messages from the last 5 days for assessment indicators
        since_date = (datetime.now() - timedelta(days=5)).strftime('%d-%b-%Y')
        target_queries = [
            'SUBJECT "assessment"',
            'SUBJECT "coding test"',
            'SUBJECT "interview"',
            'SUBJECT "test link"',
            'FROM "hackerrank"',
            'FROM "codility"',
            'FROM "testgorilla"',
            'FROM "hirevue"',
            'FROM "mettl"',
            'FROM "unstop"'
        ]

        matched_ids = set()
        for query in target_queries:
            status, data = mail.search(None, f'(UNSEEN SINCE "{since_date}" {query})')
            if status == "OK" and data[0]:
                for i in data[0].split():
                    matched_ids.add(i)

        for m_id in matched_ids:
            status, msg_data = mail.fetch(m_id, "(RFC822)")
            if status != "OK":
                continue
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = clean_header_text(msg.get("Subject", ""))
                    sender = clean_header_text(msg.get("From", ""))

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() in ["text/plain", "text/html"]:
                                try:
                                    body += part.get_payload(decode=True).decode(errors="ignore") + "\n"
                                except Exception:
                                    pass
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode(errors="ignore")
                        except Exception:
                            pass

                    parsed = process_email_message(subject, sender, body, auto_alert=True)
                    if parsed:
                        detected_count += 1
                        # Mark email as read once processed
                        mail.store(m_id, '+FLAGS', '\\Seen')

        mail.logout()
    except Exception as e:
        print(f"⚠️ [Email Monitor] IMAP connection check note: {e}")

    return detected_count
