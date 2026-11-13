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
        desc = "Strictly on-site position in Berlin."
        company = "OfficeCorp"
        location = "Berlin, Germany"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertEqual(score, 0.0)
        self.assertIn("neither Remote/WFH nor Bangalore/Karnataka/India", reasons)
        print(f"[Test Match On-Site Rejection] Score: {score} | Filtered: {reasons}")

    def test_bangalore_qa_matching(self):
        title = "QA Intern - Manual Testing"
        desc = "Looking for freshers / BCA graduates for manual test cases and defect tracking in Bangalore."
        company = "Bengaluru Tech Labs"
        location = "Bangalore, India"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertGreaterEqual(score, 50.0)
        self.assertIn("Bangalore / Karnataka / India", reasons)
        print(f"[Test Match Bangalore QA] Score: {score} | Reasons: {reasons}")

    def test_allied_support_matching(self):
        title = "Technical Support Engineer Trainee"
        desc = "Entry-level technical support, troubleshooting, bug reporting. Remote or Bangalore."
        company = "SupportDesk Co"
        location = "Remote"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertGreaterEqual(score, 50.0)
        self.assertIn("Allied Tech Support", reasons)
        print(f"[Test Match Allied Support] Score: {score} | Reasons: {reasons}")

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
