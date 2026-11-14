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
        self.assertIn("100% Online / Remote / WFH Opportunity", reasons)
        print(f"\n[Test Match 1 - WFH Tester] Score: {score} | Reasons: {reasons}")

    def test_onsite_rejection(self):
        title = "Junior Software QA Tester"
        desc = "Strictly on-site position in Berlin."
        company = "OfficeCorp"
        location = "Berlin, Germany"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertEqual(score, 0.0)
        self.assertIn("100% Online / Remote Only", reasons)
        print(f"[Test Match On-Site Rejection] Score: {score} | Filtered: {reasons}")

    def test_bangalore_onsite_rejection(self):
        # Under "Only Online" policy, physical in-office roles in Bangalore are rejected
        title = "QA Intern - Manual Testing"
        desc = "Looking for freshers / BCA graduates for manual test cases and defect tracking in our Bangalore office."
        company = "Bengaluru Tech Labs"
        location = "Bangalore, India (On-site only)"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertEqual(score, 0.0)
        self.assertIn("100% Online / Remote Only", reasons)
        print(f"[Test Match Bangalore On-Site Filtered] Score: {score} | Filtered: {reasons}")

    def test_bangalore_remote_matching(self):
        # Online / WFH roles for Bangalore companies are accepted
        title = "QA Intern - Manual Testing"
        desc = "100% Work from home / online internship for BCA graduates testing e-commerce apps."
        company = "Bengaluru Tech Labs"
        location = "Bangalore / Remote"

        score, reasons = evaluate_job_match(title, desc, company, location)
        self.assertGreaterEqual(score, 50.0)
        self.assertIn("100% Online / Remote / WFH Opportunity", reasons)
        print(f"[Test Match Bangalore Online/Remote] Score: {score} | Reasons: {reasons}")

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
        self.assertIn("100% Online / Remote / WFH Opportunity", reasons)
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

    def test_mock_api_postman_collection(self):
        import json
        collection_path = "projects/qa-ecommerce-test-suite/Varun_MS_Ecommerce_API_Tests.postman_collection.json"
        with open(collection_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["info"]["name"], "Varun M S - E-Commerce API Test Suite")
        base_url_var = next(v for v in data["variable"] if v["key"] == "base_url")
        self.assertEqual(base_url_var["value"], "https://job-auto-apply-bot.onrender.com")
        print("\n[Test Postman Mock API] Verified Postman collection is configured for 24/7 cloud testing.")

    def test_ai_self_healing_locator(self):
        sys_path_added = False
        qa_path = "projects/qa-ecommerce-test-suite/tests"
        import sys
        if qa_path not in sys.path:
            sys.path.insert(0, qa_path)
            sys_path_added = True
        try:
            from test_self_healing_playwright import AISelfHealingLocator
            healer = AISelfHealingLocator()
            candidates = [
                {"tag": "button", "id": "login-button", "class": "btn_action", "text": "Login", "type": "submit", "data-test": "login-button"},
                {"tag": "a", "id": "cancel-link", "class": "link_cancel", "text": "Cancel"}
            ]
            res = healer.deduce_healed_selector("#broken-btn", "Click the login submit button", candidates)
            self.assertIn(res["healed_selector"], ["#login-button", "[data-test='login-button']"])
            self.assertGreaterEqual(res["confidence"], 0.70)
            print("\n[Test AI Self-Healing] Verified dynamic locator recovery with confidence:", res["confidence"])
        finally:
            if sys_path_added and qa_path in sys.path:
                sys.path.remove(qa_path)

    def test_ai_root_cause_analysis_and_jira(self):
        from prep_assistant import analyze_error_and_draft_jira
        err = "playwright._impl._errors.TimeoutError: Locator.click: Timeout 5000ms exceeded waiting for locator('#checkout-button')"
        res = analyze_error_and_draft_jira(err)
        self.assertIn("UI Automation", res["error_category"])
        self.assertIn("timed out", res["rca_summary"])
        jt = res["jira_ticket"]
        self.assertEqual(jt["key"], "DEFECT-2026-QA")
        self.assertGreaterEqual(len(jt["steps_to_reproduce"]), 2)
        self.assertIn("wait_for", res["suggested_code_fix"])
        print("\n[Test AI Root Cause Analyzer & JIRA] Verified automatic defect ticketing and code patch generation.")

    def test_ai_interview_answer_evaluation(self):
        from prep_assistant import evaluate_interview_answer_ai
        ans = "I would first reproduce the bug with exact steps, take Chrome DevTools network logs and screenshots, and check against the SRS requirements document before consulting the QA lead."
        eval_res = evaluate_interview_answer_ai(1, ans)
        self.assertGreaterEqual(eval_res["score"], 7.0)
        self.assertGreaterEqual(len(eval_res["matched_keywords"]), 2)
        self.assertIn("reproduce", eval_res["matched_keywords"])
        print(f"\n[Test AI Interview Evaluation] Score: {eval_res['score']}/10 | Matched keywords: {eval_res['matched_keywords']}")

    def test_ai_gherkin_bdd_generator(self):
        from prep_assistant import generate_bdd_feature
        res = generate_bdd_feature("Shopping Cart Discount Coupon Checkout")
        self.assertIn("Feature:", res["gherkin_file"])
        self.assertIn("Scenario Outline:", res["gherkin_file"])
        self.assertIn("@given", res["pytest_steps"])
        self.assertIn("@when", res["pytest_steps"])
        self.assertIn("@then", res["pytest_steps"])
        print("\n[Test AI Gherkin BDD Generator] Verified Gherkin feature file and pytest-bdd step definitions.")

if __name__ == "__main__":
    unittest.main()
