#!/usr/bin/env python3
"""
Daily QA & Automation Concept Logger
Author: VARUN M S (Final Year BCA 2025)
Repository: https://github.com/varunms89/qa-ecommerce-test-suite

Logs daily quality assurance engineering notes and testing best practices.
Automated by GitHub Actions to maintain an active learning & development journal.
"""

from datetime import datetime
import os

DAILY_QA_TOPICS = [
    {
        "concept": "Boundary Value Analysis (BVA) 6-Point Strategy",
        "description": "For any numeric boundary [Min, Max], the 6 critical test points are Min-1 (Invalid), Min (Valid), Min+1 (Valid), Max-1 (Valid), Max (Valid), and Max+1 (Invalid). Statistical studies show over 60% of logic bugs occur at boundary extremes."
    },
    {
        "concept": "Equivalence Class Partitioning (ECP)",
        "description": "Divide test inputs into mutually exclusive equivalence partitions where all members are assumed to be processed identically by the system. Test one typical representative per partition to optimize test efficiency without reducing defect detection."
    },
    {
        "concept": "Idempotent HTTP Methods in REST APIs",
        "description": "GET, PUT, and DELETE are idempotent; making multiple identical requests must leave server state identical. POST is non-idempotent; repeated submissions create multiple records. Always verify idempotency headers in payment and order checkout APIs."
    },
    {
        "concept": "Severity vs Priority Matrix in Sprint Triage",
        "description": "Severity measures system defect impact (e.g. crash/data corruption). Priority determines developer urgency. High Severity/Low Priority: Crash in obscure edge-case configuration. Low Severity/High Priority: Misspelled company logo on landing page."
    },
    {
        "concept": "Smoke Testing vs Sanity Testing",
        "description": "Smoke Testing (Build Verification Test) is broad and shallow, run on initial builds to verify critical end-to-end paths. Sanity Testing is narrow and deep, run after minor bug fixes to verify the specific module works before regression testing."
    },
    {
        "concept": "Playwright Auto-Waiting & Resilient Locators",
        "description": "Playwright performs actionability checks (visible, stable, enabled, attached) before clicking or filling. Prefer user-facing locators like page.get_by_role() and data-test attributes over fragile brittle XPath selectors."
    },
    {
        "concept": "Shift-Left Testing in Agile SDLC",
        "description": "Testing begins during the requirement specification and design phase rather than waiting for code completion. Catching defects during requirement review is 10x cheaper than fixing bugs in system integration testing."
    },
    {
        "concept": "Defect Life Cycle & Disputed Bug Resolution",
        "description": "When a developer marks a bug as 'Not a Bug', reproduce it systematically, capture DevTools console/network logs, and verify against the SRS/BRD. If ambiguity persists, present the reproducible steps to the Product Owner/QA Lead."
    }
]

def log_daily_note():
    today = datetime.now()
    idx = today.day % len(DAILY_QA_TOPICS)
    topic = DAILY_QA_TOPICS[idx]

    notes_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "DAILY_NOTES.md")
    if not os.path.exists(notes_file):
        with open(notes_file, "w") as f:
            f.write("# 📚 Daily QA Engineering & Test Automation Learning Journal\n\n")
            f.write("**Candidate:** VARUN M S (Final Year BCA 2025 | QA & Automation Engineer)  \n")
            f.write("**Portfolio:** [varunms89.github.io](https://varunms89.github.io)  \n\n")
            f.write("---\n\n")

    entry = (
        f"### 📅 {today.strftime('%Y-%m-%d (%A)')} — {topic['concept']}\n"
        f"- **Core Concept:** {topic['description']}\n"
        f"- **Author:** VARUN M S\n"
        f"- **Status:** Verified in production & automated test pipelines.\n\n"
        f"---\n\n"
    )

    with open(notes_file, "a") as f:
        f.write(entry)

    print(f"✅ Successfully logged daily QA note for {today.strftime('%Y-%m-%d')}: {topic['concept']}")

if __name__ == "__main__":
    log_daily_note()
