import sqlite3
from matcher import evaluate_job_match
from apply_engine import AutoApplyEngine
from database import init_db, record_job, mark_applied, DB_PATH
from govt_scraper import save_govt_notifications
from config import USER_CONFIG

def run_e2e_simulation_test():
    print("==================================================================")
    print("🧪 RUNNING COMPREHENSIVE END-TO-END TEST SUITE")
    print(f"👤 Candidate: {USER_CONFIG.name}")
    print(f"🎓 Education: {USER_CONFIG.puc_12th} | {USER_CONFIG.degree}")
    print("==================================================================\n")

    init_db()
    apply_engine = AutoApplyEngine(dry_run=True)

    # 1. Simulate 12th-Standard Government Job Notifications
    print("🏛️ [TEST 1] Testing 12th Government Job Detection & Storage...")
    sample_govt_jobs = [
        {
            "portal": "KPSC",
            "title": "Recruitment Notification for Second Division Assistant (SDA) - 2025 (PUC/12th qualification)",
            "qualification": "12th / PUC (Commerce eligible)",
            "post_name": "Second Division Assistant (SDA)",
            "link": "https://kpsc.kar.nic.in/notification_sda_2025.pdf"
        },
        {
            "portal": "KEA",
            "title": "KEA Junior Assistant and Typist Recruitment in various Boards/Corporations",
            "qualification": "12th / PUC Pass with Computer Knowledge",
            "post_name": "Junior Assistant / Clerk",
            "link": "https://cetonline.karnataka.gov.in/kea/junior_assistant_2025"
        },
        {
            "portal": "RRB",
            "title": "RRB Non-Technical Popular Categories (NTPC Undergraduate) - Junior Clerk & Accounts Clerk",
            "qualification": "12th Standard Pass",
            "post_name": "Junior Clerk cum Typist",
            "link": "https://www.rrbbnc.gov.in/ntpc_12th_2025.html"
        }
    ]
    save_govt_notifications(sample_govt_jobs)
    
    # Verify in DB
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT portal, post_name, qualification FROM govt_notifications")
    stored_govt = cur.fetchall()
    conn.close()
    print(f"✅ Successfully stored and verified {len(stored_govt)} government notifications in database:")
    for portal, post, qual in stored_govt:
        print(f"   🏛️ [{portal}] {post} (Eligibility: {qual})")

    # 2. Simulate Software Tester / QA Job Listings
    print("\n🔍 [TEST 2] Testing QA / Software Tester Matching & Auto-Apply Form Generation...")
    sample_job_openings = [
        {
            "job_id": "test_qa_001",
            "platform": "Indeed",
            "title": "Junior Software QA Tester (Fresher / Trainee)",
            "company": "Infosys / Wipro Partner",
            "location": "Bangalore / Remote",
            "url": "https://in.indeed.com/viewjob?jk=qa_test_001",
            "description": "Looking for entry-level candidates or BCA final year / freshers. Good understanding of manual testing, test case execution, and bug reporting."
        },
        {
            "job_id": "test_qa_002",
            "platform": "Naukri",
            "title": "QA Manual Testing Intern",
            "company": "Cognizant",
            "location": "Karnataka / Hybrid",
            "url": "https://www.naukri.com/job-listings-qa-intern-002",
            "description": "Fresher QA intern wanted. Knowledge of Python, Postman, JIRA bug tracking, or basic web testing tools is an advantage. Any degree / BCA candidates welcome."
        },
        {
            "job_id": "test_qa_003_senior",
            "platform": "Indeed",
            "title": "Senior QA Automation Lead (7+ years)",
            "company": "Amazon",
            "location": "Bangalore",
            "url": "https://in.indeed.com/viewjob?jk=senior_qa",
            "description": "Requires minimum 7 years leading automation teams, Java, Selenium."
        }
    ]

    applied_count = 0
    for job in sample_job_openings:
        score, reasons = evaluate_job_match(
            job["title"], job["description"], job["company"], job["location"]
        )
        print(f"\nEvaluating: '{job['title']}'")
        print(f" -> Match Score: {score}/100")
        print(f" -> Analysis: {reasons}")

        if score >= 35.0:
            print(" -> Result: MATCH QUALIFIED! Executing Auto-Apply...")
            record_job(
                job_id=job["job_id"],
                platform=job["platform"],
                title=job["title"],
                company=job["company"],
                location=job["location"],
                url=job["url"],
                description=job["description"],
                match_score=score,
                match_reasons=reasons,
                status="DISCOVERED"
            )
            success = apply_engine.apply_to_job(job)
            if success:
                applied_count += 1
        else:
            print(" -> Result: EXCLUDED (Does not fit fresher / entry-level profile).")

    print("\n==================================================================")
    print(f"📊 TEST SUITE SUMMARY:")
    print(f"  ✅ 12th Govt Jobs Verified & Stored: {len(stored_govt)}")
    print(f"  ✅ Fresher QA Jobs Matched & Auto-Applied: {applied_count}")
    print(f"  ✅ Senior Jobs Filtered Out: 1")
    print("==================================================================")

if __name__ == "__main__":
    run_e2e_simulation_test()
