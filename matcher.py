import re
from typing import Dict, Any, Tuple
from config import USER_CONFIG

def evaluate_job_match(title: str, description: str, company: str, location: str) -> Tuple[float, str]:
    """
    EXPANDED MATCHING STRATEGY (Option C):
    1. Roles: Software Tester / QA / Quality Assurance / Test Engineer
              + Allied Tech Roles: Technical Support, QA Support, Application Support, Junior Developer / Trainee.
    2. Location / Work Mode: Remote / Work From Home OR Bangalore / Karnataka / India (Hybrid & On-site).
    3. Seniority: Rejects Senior, Lead, Principal, Manager, 5+ years.
    """
    full_text = f"{title} {description} {company} {location}".lower()
    title_lower = title.lower()

    # 1. Seniority Check (Hard Filter)
    seniority_flags = ["senior", "sr.", "lead", "principal", "manager", "architect", "head of", "director", "5+ years", "6+ years", "7+ years", "10+ years"]
    for flag in seniority_flags:
        if flag in title_lower:
            return 0.0, f"Rejected: Senior level role ({flag})"

    # 2. Role Title Matching
    primary_qa_keywords = ["tester", "qa", "quality assurance", "test engineer", "software testing", "test analyst", "manual test"]
    allied_keywords = [
        "support engineer", "technical support", "tech support", "application support", 
        "qa support", "it support", "trainee", "qa intern", "testing intern", "test intern",
        "junior developer", "junior software", "graduate engineer", "software intern", "developer intern", "data trainee"
    ]

    is_primary_qa = any(kw in title_lower for kw in primary_qa_keywords)
    is_allied = any(kw in title_lower for kw in allied_keywords)

    # Exclude non-tech intern roles like marketing, hr, people ops, sales intern
    non_tech_flags = ["marketing", "recruitment", "human resources", "people ops", "talent", "electrical", "power electronics", "growth associate", "ux research", "copywriter"]
    if any(nt in title_lower for nt in non_tech_flags):
        return 0.0, "Rejected: Non-technical role"

    if not (is_primary_qa or is_allied):
        # Check description for strong QA/testing context
        if any(kw in description.lower() for kw in ["software testing", "manual testing", "qa testing", "test cases", "bug reporting"]):
            is_primary_qa = True
        else:
            return 0.0, "Rejected: Role is neither QA/Testing nor allied technical support/trainee role"

    # 3. Location / Work Mode Matching
    wfh_terms = ["remote", "work from home", "wfh", "anywhere", "telecommute", "home-based", "virtual", "worldwide"]
    india_loc_terms = ["bangalore", "bengaluru", "karnataka", "india", "hassan", "hyderabad", "chennai", "pune"]

    is_remote = any(wfh in full_text for wfh in wfh_terms)
    is_local_india = any(loc in full_text for loc in india_loc_terms)

    if not (is_remote or is_local_india):
        return 0.0, "Rejected: Location is neither Remote/WFH nor Bangalore/Karnataka/India"

    # 4. Score Calculation
    score = 40.0
    reasons = []

    if is_primary_qa:
        score += 25.0
        reasons.append("🎯 Direct Software Tester / QA role")
    else:
        score += 15.0
        reasons.append("🛠️ Allied Tech Support / Trainee role")

    if is_remote:
        score += 15.0
        reasons.append("🏠 Work From Home (Remote)")
    if is_local_india:
        score += 10.0
        reasons.append("📍 Bangalore / Karnataka / India location")

    # Fresher / Entry-level boost
    if any(k in full_text for k in ["fresher", "intern", "trainee", "entry level", "junior", "graduate", "0-1", "0-2"]):
        score += 10.0
        reasons.append("Matches entry-level / intern / fresher")

    # Skills matching
    skills_hit = [s for s in ["manual testing", "test cases", "jira", "postman", "bug", "python", "sql", "troubleshooting", "customer support"] if s in full_text]
    if skills_hit:
        score += 10.0
        reasons.append(f"Skills matched: {', '.join(skills_hit[:4])}")

    return min(score, 100.0), "; ".join(reasons)
