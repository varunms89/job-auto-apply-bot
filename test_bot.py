import unittest
from matcher import evaluate_job_match
from apply_engine import AutoApplyEngine
from config import USER_CONFIG

class TestJobBot(unittest.TestCase):
    def test_qa_fresher_job_matching(self):
        title = "Junior Software QA Tester - Remote / Work From Home"
        desc = "100% Remote / Work from home position for freshers and BCA graduates. Knowledge of manual testing, test cases, and bug tracking."
        company = "TechCorp Solutions"
        location = "Remote / Anywhere"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertGreaterEqual(score, 50.0)
        self.assertIn("Software Tester", reasons)
        self.assertIn("Work From Home", reasons)
        print(f"\n[Test Match 1 - WFH Tester] Score: {score} | Reasons: {reasons}")

    def test_onsite_rejection(self):
        title = "Junior Software QA Tester"
        desc = "Strictly on-site position at office."
        company = "OfficeCorp"
        location = "Mumbai Office Only"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertEqual(score, 0.0)
        self.assertIn("does not offer Work From Home", reasons)
        print(f"[Test Match On-Site Rejection] Score: {score} | Filtered: {reasons}")

    def test_auto_apply_payload(self):
        engine = AutoApplyEngine(dry_run=True)
        job = {
            "job_id": "test_101",
            "title": "Software Tester Intern",
            "company": "Infosys",
            "platform": "Indeed",
            "url": "https://example.com/job"
        }
        payload = engine.prepare_application_payload(job)
        self.assertEqual(payload["full_name"], "VARUN M S")
        self.assertEqual(payload["email"], "msvarun89@gmail.com")
        self.assertIn("BCA", payload["education"]["degree"])
        self.assertIn("VARUN M S", payload["cover_letter"])
        print("\n[Test Application Payload] Successfully prepared custom cover letter and applicant details.")

if __name__ == "__main__":
    unittest.main()
