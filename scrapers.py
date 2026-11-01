import urllib.request
import json
import re
import ssl
from typing import List, Dict

# Create unverified SSL context for gov sites with older SSL chains
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

def fetch_json(url: str) -> Dict:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=12) as resp:
        return json.loads(resp.read().decode('utf-8'))

def search_remoteok_jobs() -> List[Dict]:
    """
    RemoteOK open API for QA and developer jobs.
    """
    jobs = []
    try:
        url = "https://remoteok.com/api?tag=qa"
        data = fetch_json(url)
        for item in data:
            if not isinstance(item, dict) or 'position' not in item:
                continue
            title = item.get('position', '')
            company = item.get('company', '')
            url_link = item.get('url', f"https://remoteok.com/l/{item.get('id', '')}")
            desc = item.get('description', '')
            clean_desc = re.sub(r'<[^>]+>', ' ', desc)[:2000]

            job_id = f"remoteok_{item.get('id', hash(url_link))}"
            jobs.append({
                "job_id": job_id,
                "platform": "RemoteOK",
                "title": title,
                "company": company,
                "location": "Remote / Worldwide",
                "url": url_link,
                "description": clean_desc
            })
    except Exception as e:
        print(f"[RemoteOK] Notice: {e}")
    return jobs

def search_arbeitnow_jobs() -> List[Dict]:
    """
    Arbeitnow open jobs API (QA, testing, tech).
    """
    jobs = []
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        data = fetch_json(url)
        for item in data.get('data', []):
            title = item.get('title', '')
            company = item.get('company_name', '')
            url_link = item.get('url', '')
            location = item.get('location', 'Remote')
            desc = re.sub(r'<[^>]+>', ' ', item.get('description', ''))[:2000]

            # Check if relevant to QA, testing, or entry-level
            text_to_check = (title + " " + desc).lower()
            if any(k in text_to_check for k in ["qa", "test", "quality", "junior", "trainee", "intern"]):
                jobs.append({
                    "job_id": f"arbeit_{item.get('slug', hash(url_link))}",
                    "platform": "ArbeitNow",
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": url_link,
                    "description": desc
                })
    except Exception as e:
        print(f"[ArbeitNow] Notice: {e}")
    return jobs

def search_remotive_jobs() -> List[Dict]:
    """
    Remotive API for remote QA and testing jobs.
    """
    jobs = []
    try:
        url = "https://remotive.com/api/remote-jobs?search=qa"
        data = fetch_json(url)
        for item in data.get('jobs', []):
            title = item.get('title', '')
            company = item.get('company_name', '')
            url_link = item.get('url', '')
            location = item.get('candidate_required_location', 'Remote / Worldwide')
            desc = re.sub(r'<[^>]+>', ' ', item.get('description', ''))[:2000]

            jobs.append({
                "job_id": f"remotive_{item.get('id', hash(url_link))}",
                "platform": "Remotive",
                "title": title,
                "company": company,
                "location": location,
                "url": url_link,
                "description": desc
            })
    except Exception as e:
        print(f"[Remotive] Notice: {e}")
    return jobs

def search_jobicy_jobs() -> List[Dict]:
    """
    Jobicy API for remote engineering & testing jobs.
    """
    jobs = []
    try:
        url = "https://jobicy.com/api/v2/remote-jobs?count=50&industry=engineering"
        data = fetch_json(url)
        for item in data.get('jobs', []):
            title = item.get('jobTitle', '')
            company = item.get('companyName', '')
            url_link = item.get('url', '')
            location = item.get('jobGeo', 'Remote / Worldwide')
            desc = re.sub(r'<[^>]+>', ' ', item.get('jobExcerpt', ''))[:2000]

            jobs.append({
                "job_id": f"jobicy_{item.get('id', hash(url_link))}",
                "platform": "Jobicy",
                "title": title,
                "company": company,
                "location": location,
                "url": url_link,
                "description": desc
            })
    except Exception as e:
        print(f"[Jobicy] Notice: {e}")
    return jobs

def search_all_portals() -> List[Dict]:
    results = []
    print("  -> Querying open tech API job feeds (RemoteOK, ArbeitNow, Remotive, Jobicy)...")
    results.extend(search_remoteok_jobs())
    results.extend(search_arbeitnow_jobs())
    results.extend(search_remotive_jobs())
    results.extend(search_jobicy_jobs())

    # Deduplicate
    seen = set()
    unique_jobs = []
    for j in results:
        if j['job_id'] not in seen:
            seen.add(j['job_id'])
            unique_jobs.append(j)
    return unique_jobs
