import sys
import time
from database import init_db, record_job, is_job_applied_or_seen, get_job_stats
from scrapers import search_all_portals
from matcher import evaluate_job_match
from apply_engine import AutoApplyEngine
from config import USER_CONFIG

def run_job_bot_cycle(auto_apply: bool = True):
    print("==================================================================")
    print(f"🤖 STARTING SOFTWARE TESTER / QA JOB AUTO-APPLY BOT")
    print(f"👤 Candidate: {USER_CONFIG.name}")
    print(f"🎓 Degree: {USER_CONFIG.degree} ({USER_CONFIG.college})")
    print(f"🎯 Target Roles: Software Tester, QA Intern, Manual Tester, QA Trainee")
    print(f"📍 Location: Bangalore / Karnataka / Remote / Worldwide")
    print("==================================================================")

    init_db()
    apply_engine = AutoApplyEngine(dry_run=True)

    # 1. Tech / QA Jobs Search
    print("\n🔍 Fetching latest Software Tester / QA job postings across platforms...")
    jobs = search_all_portals()
    print(f"  -> Discovered {len(jobs)} active job listings.")

    matched_count = 0
    applied_count = 0

    # 3. Match and Apply
    for job in jobs:
        job_id = job["job_id"]
        title = job["title"]
        company = job["company"]
        location = job["location"]
        url = job["url"]
        desc = job["description"]

        if is_job_applied_or_seen(job_id):
            continue

        score, reasons = evaluate_job_match(title, desc, company, location)

        # Record in DB
        record_job(
            job_id=job_id,
            platform=job["platform"],
            title=title,
            company=company,
            location=location,
            url=url,
            description=desc,
            match_score=score,
            match_reasons=reasons,
            status="DISCOVERED"
        )

        # Qualification threshold: Score >= 40 indicates strong Tester / QA Fresher match
        if score >= 35.0:
            matched_count += 1
            print(f"\n🎯 [MATCH FOUND] Score: {score}/100 | {title} at {company}")
            print(f"   Reason: {reasons}")
            
            if auto_apply:
                success = apply_engine.apply_to_job(job)
                if success:
                    applied_count += 1

    print("\n==================================================================")
    print("📊 CYCLE SUMMARY")
    print(f"  - Total New QA Listings Evaluated: {len(jobs)}")
    print(f"  - Qualified Tester/QA Matches: {matched_count}")
    print(f"  - Applications Prepared/Processed: {applied_count}")
    print("==================================================================")

    # Automatically dispatch report to Telegram
    try:
        from telegram_notifier import dispatch_report
        print("\n📲 Dispatching cycle summary to Telegram...")
        dispatch_report()
    except Exception as e:
        print(f"Telegram notice: {e}")

if __name__ == "__main__":
    run_job_bot_cycle(auto_apply=True)
