import urllib.request
import json
import re
import os
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

def search_linkedin_jobs() -> List[Dict]:
    """
    Scrapes real-time Software Tester & QA jobs from LinkedIn for India & Remote.
    """
    jobs = []
    queries = [
        # Remote / Online Focused Queries (f_WT=2 is LinkedIn filter for Remote/Work From Home)
        ("Software%20Tester", "Remote"),
        ("QA%20Intern", "Remote"),
        ("AI%20Intern", "Remote"),
        ("Machine%20Learning%20Intern", "Remote"),
        ("Python%20Intern", "Remote"),
        ("Software%20Developer%20Intern", "Remote"),
        # Regional Tech Hub Queries
        ("AI%20Intern", "India"),
        ("QA%20Intern", "Bengaluru"),
        ("Software%20Tester", "Bengaluru"),
        ("Machine%20Learning%20Intern", "Bengaluru")
    ]
    
    linkedin_cookie = os.environ.get("LINKEDIN_LI_AT", "")

    for keyword, location in queries:
        try:
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location={location}&f_TPR=r86400&start=0"
            req_headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            }
            if linkedin_cookie:
                req_headers['Cookie'] = f"li_at={linkedin_cookie};"

            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                
                # Split by job card
                cards = html.split('base-card')
                for card in cards[1:]:
                    title_m = re.search(r'<h3 class=\"base-search-card__title\">[\s\n]*([^<]+)[\s\n]*</h3>', card)
                    link_m = re.search(r'href=\"(https://[a-z]+\.linkedin\.com/jobs/view/[^\"]+)\"', card)
                    company_m = re.search(r'<h4 class=\"base-search-card__subtitle\">[\s\S]*?</h4>', card)
                    
                    if title_m and link_m:
                        clean_title = title_m.group(1).strip()
                        clean_url = link_m.group(1).split('?')[0]
                        clean_company = re.sub(r'<[^>]+>', '', company_m.group(0)).strip() if company_m else "LinkedIn Company"
                        job_id = f"li_{re.sub(r'[^0-9]', '', clean_url)[-12:] or abs(hash(clean_url))}"

                        jobs.append({
                            "job_id": job_id,
                            "platform": "LinkedIn",
                            "title": clean_title,
                            "company": clean_company,
                            "location": location,
                            "url": clean_url,
                            "description": f"LinkedIn Job: {clean_title} at {clean_company} in {location}. Direct link: {clean_url}"
                        })
        except Exception as e:
            print(f"[LinkedIn Scraper] Notice for {keyword}/{location}: {e}")
            
    return jobs

def search_internshala_internships() -> List[Dict]:
    """
    Scrapes high-volume Indian online/remote internships from Internshala
    for AI, Python, Software Testing / QA, and Bangalore tech internships.
    """
    categories = [
        ("work-from-home-artificial-intelligence-ai-internships", "Artificial Intelligence Intern", "Work From Home / Remote"),
        ("work-from-home-software-testing-internships", "Software Tester / QA Intern", "Work From Home / Remote"),
        ("work-from-home-python-django-internships", "Python Developer Intern", "Work From Home / Remote"),
        ("computer-science-internship-in-bangalore", "CS / Software Intern", "Bangalore, India")
    ]
    jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    for slug, default_title, default_loc in categories:
        try:
            url = f"https://internshala.com/internships/{slug}/"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')

                raw_cards = re.findall(r'<div[^>]*id=\"individual_internship_[0-9]+\"[^>]*>[\s\S]*?(?=<div[^>]*id=\"individual_internship_[0-9]+\"|$)', html)
                for card in raw_cards:
                    t_m = re.search(r'<a[^>]*job-title-href[^>]*>[\s\S]*?</a>', card)
                    c_m = re.search(r'<p[^>]*class=[\"\'][^\"\']*company-name[^\"\']*[\"\'][^>]*>[\s\n]*([^<]+)[\s\n]*</p>', card)
                    if not c_m:
                        c_m = re.search(r'<a[^>]*class=[\"\'][^\"\']*company-name[^\"\']*[\"\'][^>]*>[\s\n]*([^<]+)[\s\n]*</a>', card)
                    loc_m = re.search(r'<a[^>]*class=[\"\'][^\"\']*location_link[^\"\']*[\"\'][^>]*>[\s\n]*([^<]+)[\s\n]*</a>', card)

                    if t_m:
                        title_text = re.sub(r'<[^>]+>', '', t_m.group(0)).strip()
                        if "internship" not in title_text.lower():
                            title = f"{title_text} Intern"
                        else:
                            title = title_text
                        
                        href_m = re.search(r'href=[\"\']([^\"\']+)[\"\']', t_m.group(0))
                        clean_href = href_m.group(1).split('?')[0] if href_m else ""
                        if not clean_href:
                            continue
                        
                        full_url = "https://internshala.com" + clean_href
                        company = c_m.group(1).strip() if c_m else "Internshala Partner Company"
                        loc = loc_m.group(1).strip() if loc_m else default_loc

                        # Unique ID from Internshala URL ending
                        num_id = re.sub(r'[^0-9]', '', clean_href)[-10:] or abs(hash(full_url))
                        job_id = f"internshala_{num_id}"

                        desc = f"Internshala Internship: {title} at {company}. Location: {loc}. Online WFH student internship. Apply directly: {full_url}"

                        jobs.append({
                            "job_id": job_id,
                            "platform": "Internshala",
                            "title": title,
                            "company": company,
                            "location": loc,
                            "url": full_url,
                            "description": desc
                        })
        except Exception as e:
            print(f"[Internshala Scraper] Notice for {slug}: {e}")

    return jobs

def search_all_portals() -> List[Dict]:
    results = []
    print("  -> Querying open tech API job feeds (RemoteOK, ArbeitNow, Remotive, Jobicy, LinkedIn, Internshala)...")
    results.extend(search_remoteok_jobs())
    results.extend(search_arbeitnow_jobs())
    results.extend(search_remotive_jobs())
    results.extend(search_jobicy_jobs())
    results.extend(search_linkedin_jobs())
    results.extend(search_internshala_internships())

    # Deduplicate
    seen = set()
    unique_jobs = []
    for j in results:
        if j['job_id'] not in seen:
            seen.add(j['job_id'])
            unique_jobs.append(j)
    return unique_jobs
