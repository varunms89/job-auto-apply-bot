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
        self.assertIn("TOP PREFERENCE: Online / Remote / WFH", reasons)
        print(f"\n[Test Match 1 - WFH Tester] Score: {score} | Reasons: {reasons}")

    def test_onsite_rejection(self):
        title = "Junior Software QA Tester"
        desc = "Strictly on-site position in Berlin."
        company = "OfficeCorp"
        location = "Berlin, Germany"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertEqual(score, 0.0)
        self.assertIn("neither Online/Remote/WFH nor Bangalore/Karnataka/India", reasons)
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

    def test_ai_internship_matching(self):
        title = "Artificial Intelligence Intern"
        desc = "Seeking an AI intern with Python skills, familiarity with machine learning libraries and generative AI tools."
        company = "AI Nexus Labs"
        location = "Bangalore / Remote"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertGreaterEqual(score, 60.0)
        self.assertIn("AI & Programming Internship", reasons)
        print(f"[Test Match AI Internship] Score: {score} | Reasons: {reasons}")

    def test_python_programming_intern_matching(self):
        title = "Python Developer Intern"
        desc = "Exciting internship opportunity for BCA/BTech freshers to work on Python backend and AI apps."
        company = "InnoTech Solutions"
        location = "Remote"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertGreaterEqual(score, 60.0)
        self.assertIn("AI & Programming Internship", reasons)
        print(f"[Test Match Python Intern] Score: {score} | Reasons: {reasons}")

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

    def test_assessment_email_detection(self):
        from email_monitor import process_email_message
        subject = "Invitation to Online Assessment from Siemens"
        sender = "talent@siemens.com"
        body = """
        Dear Candidate,
        You are invited to complete your online coding test on HackerRank.
        Please complete the assessment before Nov 18, 2026.
        Assessment Link: https://www.hackerrank.com/tests/siemens-intern-qa-2026
        Best regards,
        Siemens Recruiting
        """
        # test with auto_alert=False so we don't spam Telegram during unit test
        result = process_email_message(subject, sender, body, auto_alert=False)
        self.assertIsNotNone(result)
        self.assertEqual(result["platform"], "HackerRank")
        self.assertIn("hackerrank.com", result["test_url"])
        self.assertIn("Siemens", result["company"])
        print(f"\n[Test Email Assessment Parser] Detected: {result['company']} | {result['platform']} | {result['deadline_or_time']}")

    def test_prep_assistant_modules(self):
        from prep_assistant import get_prep_module
        qa_mod = get_prep_module("qa")
        py_mod = get_prep_module("python")
        ai_mod = get_prep_module("ai")

        self.assertIn("Testing & QA", qa_mod["title"])
        self.assertIn("Python", py_mod["title"])
        self.assertIn("Artificial Intelligence", ai_mod["title"])
        self.assertGreaterEqual(len(qa_mod["sections"]), 3)
        self.assertGreaterEqual(len(py_mod["sections"]), 2)
        print("\n[Test Prep Assistant] Verified study guides for QA, Python Coding, and AI/ML.")

    def test_internshala_matching(self):
        title = "Artificial Intelligence (AI) Intern"
        desc = "Internshala Internship: Artificial Intelligence (AI) at TechCorp. Location: Work From Home. Online WFH student internship."
        company = "Pledge India Foundation"
        location = "Work From Home / Remote"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertGreaterEqual(score, 70.0)
        self.assertIn("TOP PREFERENCE: Online / Remote / WFH", reasons)
        print(f"\n[Test Internshala Match] Score: {score} | Reasons: {reasons}")

    def test_hr_screening_and_starring(self):
        from prep_assistant import HR_SCREENING_QUESTIONS
        from database import toggle_job_star
        self.assertGreaterEqual(len(HR_SCREENING_QUESTIONS), 4)
        self.assertIn("Varun M S", HR_SCREENING_QUESTIONS[0]["script"])
        self.assertIn("Government Science College", HR_SCREENING_QUESTIONS[0]["script"])

        # Toggle star test
        st1 = toggle_job_star(1)
        st2 = toggle_job_star(1)
        self.assertNotEqual(st1, st2)
        print("\n[Test HR Screening & Starring] Verified HR script and star toggle database operations.")

    def test_ai_test_case_generator(self):
        from prep_assistant import generate_test_cases
        coupon_cases = generate_test_cases("Coupon discount")
        upi_cases = generate_test_cases("UPI Payment")
        generic_cases = generate_test_cases("Flight seat selection")

        self.assertGreaterEqual(len(coupon_cases), 5)
        self.assertGreaterEqual(len(upi_cases), 5)
        self.assertGreaterEqual(len(generic_cases), 5)
        self.assertIn("TC_CPN_", coupon_cases[0]["id"])
        self.assertIn("TC_PAY_", upi_cases[0]["id"])
        print("\n[Test AI Test Case Generator] Verified rule-based IEEE test case authoring for QA.")

if __name__ == "__main__":
    unittest.main()
