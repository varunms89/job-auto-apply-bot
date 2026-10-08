import re
from typing import Dict, Any, Tuple
from config import USER_CONFIG

def evaluate_job_match(title: str, description: str, company: str, location: str) -> Tuple[float, str]:
    """
    Evaluates how well a job fits Varun M S:
    - Target: Software Tester / QA / Manual Testing / QA Intern / BCA Fresher
    - Location: Any / Karnataka / Bangalore / Remote
    - Experience: 0-1 years / Fresher / Intern
    Returns: (score between 0 and 100, reason string)
    """
    score = 0.0
    reasons = []

    full_text = f"{title} {description} {company}".lower()

    # 1. Seniority Check (Hard filter: penalties for Senior/Lead/Manager/5+ yrs)
    seniority_flags = ["senior", "sr.", "lead", "principal", "manager", "architect", "5+ years", "6+ years", "7+ years", "10+ years"]
    for flag in seniority_flags:
        if flag in title.lower():
            return 0.0, f"Role requires senior experience: {flag}"

    # 2. Fresher / Entry Level / Intern bonus
    fresher_flags = ["intern", "internship", "fresher", "trainee", "entry level", "junior", "jr", "graduate", "0-1", "0-2", "bca", "any graduate"]
    for flag in fresher_flags:
        if flag in full_text:
            score += 15.0
            reasons.append(f"Matches entry-level keyword: '{flag}'")
            break

    # 3. Role Title Matching (QA / Tester / Software Tester)
    tester_keywords = ["tester", "qa", "quality assurance", "test engineer", "software testing", "test analyst", "manual test"]
    matched_title = False
    for kw in tester_keywords:
        if kw in title.lower():
            score += 35.0
            reasons.append(f"Title directly matches target QA role: '{kw}'")
            matched_title = True
            break
            
    if not matched_title:
        # Check if generic developer or trainee
        if any(dev in title.lower() for dev in ["trainee", "associate", "junior developer", "python", "software engineer"]):
            score += 15.0
            reasons.append("General entry-level software role")

    # 4. Skills matching in Job Description
    skill_hits = []
    core_skills = ["manual testing", "automation", "test cases", "jira", "selenium", "bug", "python", "api testing", "postman", "sql", "testing"]
    for s in core_skills:
        if s in full_text:
            skill_hits.append(s)
            score += 5.0
            
    if skill_hits:
        reasons.append(f"Skills present: {', '.join(skill_hits[:5])}")

    # Cap score at 100
    final_score = min(score, 100.0)

    # 6. Remote / Work From Home (WFH) Preference Boost
    wfh_terms = ["remote", "work from home", "wfh", "anywhere", "telecommute", "home-based", "virtual"]
    is_wfh = any(term in full_text or term in location.lower() for term in wfh_terms)
    
    if is_wfh:
        final_score += 25.0
        reasons.append("⭐️ Matches Work From Home (WFH) / Remote preference")
    else:
        # If explicitly on-site only with no remote flexibility, give slight penalty
        if any(term in full_text for term in ["strictly on-site", "relocation required", "must work in office"]):
            final_score -= 20.0
            reasons.append("Strict on-site requirement")

    final_score = max(0.0, min(final_score, 100.0))
    return final_score, "; ".join(reasons)
