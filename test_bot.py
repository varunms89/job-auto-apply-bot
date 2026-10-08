import unittest
from matcher import evaluate_job_match
from apply_engine import AutoApplyEngine
from config import USER_CONFIG

class TestJobBot(unittest.TestCase):
    def test_qa_fresher_job_matching(self):
        title = "Junior Software QA Tester - Fresher / Trainee"
        desc = "Looking for entry level candidates or BCA graduates with basic testing knowledge, manual testing, and bug tracking."
        company = "TechCorp Solutions"
        location = "Bangalore"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertGreaterEqual(score, 50.0)
        self.assertIn("QA role", reasons)
        print(f"\n[Test Match 1] Score: {score} | Reasons: {reasons}")

    def test_senior_role_filter(self):
        title = "Senior QA Automation Lead (8+ years experience)"
        desc = "Must have 8+ years leading testing teams."
        score, reasons = evaluate_job_match(title, desc, "Enterprise Inc", "Bangalore")
        self.assertEqual(score, 0.0)
        print(f"[Test Match 2 - Senior Filter] Score: {score} | Filtered: {reasons}")

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
