import urllib.request
import re
from typing import List, Dict
import sqlite3
import os
from database import DB_PATH

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 12th Standard / PUC Government Exam Keywords
GOVT_12TH_KEYWORDS = [
    "12th", "puc", "intermediate", "sda", "second division",
    "junior assistant", "clerk", "typist", "data entry",
    "chsl", "ntpc", "constable", "postal", "railway"
]

def is_12th_basis_notification(title: str) -> bool:
    title_lower = title.lower()
    return any(kw in title_lower for kw in GOVT_12TH_KEYWORDS)

def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='ignore')

def check_kpsc_12th_jobs() -> List[Dict]:
    """
    KPSC (Karnataka Public Service Commission) - SDA, Group C (12th/PUC level)
    """
    notifications = []
    url = "https://kpsc.kar.nic.in"
    try:
        html = fetch_html(url)
        matches = re.findall(r'<a[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>', html, re.IGNORECASE)
        for link, text in matches:
            text_clean = re.sub(r'\s+', ' ', text).strip()
            if any(k in text_clean.lower() for k in ["sda", "second division", "group c", "puc", "12th", "notification", "recruitment"]):
                full_link = link if link.startswith("http") else f"https://kpsc.kar.nic.in/{link.lstrip('/')}"
                notifications.append({
                    "portal": "KPSC",
                    "title": text_clean,
                    "qualification": "12th / PUC",
                    "post_name": "SDA / Group C Post",
                    "link": full_link
                })
    except Exception as e:
        print(f"[KPSC 12th Tracker] Notice: {e}")
    return notifications

def check_kea_12th_jobs() -> List[Dict]:
    """
    KEA (Karnataka Examination Authority) - Junior Assistant, Clerks (12th/PUC basis)
    """
    notifications = []
    url = "https://cetonline.karnataka.gov.in/kea/"
    try:
        html = fetch_html(url)
        matches = re.findall(r'<a[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>', html, re.IGNORECASE)
        for link, text in matches:
            text_clean = re.sub(r'\s+', ' ', text).strip()
            if any(k in text_clean.lower() for k in ["junior assistant", "clerk", "recruitment", "sda", "puc", "12th"]):
                full_link = link if link.startswith("http") else f"https://cetonline.karnataka.gov.in/kea/{link.lstrip('/')}"
                notifications.append({
                    "portal": "KEA",
                    "title": text_clean,
                    "qualification": "12th / PUC",
                    "post_name": "Junior Assistant / Clerk",
                    "link": full_link
                })
    except Exception as e:
        print(f"[KEA 12th Tracker] Notice: {e}")
    return notifications

def check_rrb_ssc_12th_jobs() -> List[Dict]:
    """
    Central Government Jobs:
    - SSC CHSL (Combined Higher Secondary Level - 12th pass)
    - RRB NTPC Under Graduate (Junior Clerk, Accounts Clerk, Trains Clerk - 12th pass)
    """
    notifications = []
    # Central government portals & regional RRB boards (RRB Bangalore)
    sources = [
        ("RRB Bangalore", "https://www.rrbbnc.gov.in", ["ntpc", "12th", "clerk", "typist", "technician"]),
        ("SSC", "https://ssc.gov.in", ["chsl", "12th", "data entry", "clerk", "stenographer"])
    ]
    for portal_name, portal_url, keywords in sources:
        try:
            html = fetch_html(portal_url)
            matches = re.findall(r'<a[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>', html, re.IGNORECASE)
            for link, text in matches:
                text_clean = re.sub(r'\s+', ' ', text).strip()
                if any(kw in text_clean.lower() for kw in keywords):
                    full_link = link if link.startswith("http") else f"{portal_url}/{link.lstrip('/')}"
                    notifications.append({
                        "portal": portal_name,
                        "title": text_clean,
                        "qualification": "12th Standard / Higher Secondary",
                        "post_name": "12th Level Central Govt Post",
                        "link": full_link
                    })
        except Exception as e:
            print(f"[{portal_name} 12th Tracker] Notice: {e}")
    return notifications

def track_all_12th_govt_openings() -> List[Dict]:
    results = []
    results.extend(check_kpsc_12th_jobs())
    results.extend(check_kea_12th_jobs())
    results.extend(check_rrb_ssc_12th_jobs())
    return results

def save_govt_notifications(items: List[Dict]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for item in items:
        cursor.execute("""
            INSERT OR IGNORE INTO govt_notifications 
            (portal, notification_title, qualification, post_name, link)
            VALUES (?, ?, ?, ?, ?)
        """, (item['portal'], item['title'], item.get('qualification', '12th Pass'), item.get('post_name', 'Govt Post'), item['link']))
    conn.commit()
    conn.close()
