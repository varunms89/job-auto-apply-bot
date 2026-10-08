import re
from typing import Dict, Any, Tuple
from config import USER_CONFIG

def evaluate_job_match(title: str, description: str, company: str, location: str) -> Tuple[float, str]:
    """
    STRICT FILTER: ONLY SOFTWARE TESTER / QA + ONLY WORK FROM HOME / REMOTE.
    Any job that is NOT testing, or NOT remote/work from home is strictly rejected.
    """
    full_text = f"{title} {description} {company} {location}".lower()

    # 1. Hard Check 1: MUST BE SOFTWARE TESTING / QA ROLE
    tester_keywords = ["tester", "qa", "quality assurance", "test engineer", "software testing", "test analyst", "manual test"]
    if not any(kw in title.lower() for kw in tester_keywords):
        return 0.0, "Rejected: Role is not Software Testing / QA"

    # 2. Hard Check 2: MUST BE WORK FROM HOME / REMOTE
    wfh_terms = ["remote", "work from home", "wfh", "anywhere", "telecommute", "home-based", "virtual", "worldwide"]
    if not any(wfh in full_text for wfh in wfh_terms):
        return 0.0, "Rejected: Job does not offer Work From Home (Remote)"

    # 3. Seniority Check (Hard filter: Reject senior roles)
    seniority_flags = ["senior", "sr.", "lead", "principal", "manager", "architect", "5+ years", "6+ years", "7+ years", "10+ years"]
    for flag in seniority_flags:
        if flag in title.lower():
            return 0.0, f"Rejected: Senior level role ({flag})"

    score = 50.0  # Base qualification passed (Tester + WFH)
    reasons = ["✅ Strictly Software Tester role", "🏠 100% Work From Home (Remote)"]

    # 4. Fresher / Entry Level Bonus
    if any(k in full_text for k in ["fresher", "intern", "trainee", "entry level", "junior", "0-1", "0-2"]):
        score += 25.0
        reasons.append("Matches entry-level / intern / fresher")

    # 5. Core Testing Skills
    skills_hit = [s for s in ["manual testing", "test cases", "jira", "postman", "bug", "python"] if s in full_text]
    if skills_hit:
        score += 20.0
        reasons.append(f"Skills matched: {', '.join(skills_hit[:4])}")

    return min(score, 100.0), "; ".join(reasons)
