import re
from typing import Dict, Any, Tuple
from config import USER_CONFIG

def evaluate_job_match(title: str, description: str, company: str, location: str) -> Tuple[float, str]:
    """
    STRICT 100% ONLINE / REMOTE / WFH MATCHING STRATEGY:
    1. Location / Work Mode: 100% ONLINE / REMOTE / WORK FROM HOME (WFH) ONLY.
       Rejects all physical on-site or in-office jobs, even if based in Bangalore/India.
    2. Roles: Software Tester / QA / Quality Assurance / Test Engineer
              + Allied Tech Roles: AI/Python Intern, Technical Support, Application Support, Junior Developer / Trainee.
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
    
    # AI & Programming Language Internships / Entry-level roles
    ai_and_programming_keywords = [
        "ai intern", "artificial intelligence intern", "machine learning intern", "ml intern",
        "genai intern", "generative ai", "ai trainee", "ai engineer intern", "ai research intern",
        "python intern", "python developer intern", "software intern", "developer intern",
        "software engineering intern", "software developer intern", "programming intern",
        "backend intern", "frontend intern", "web development intern", "coding intern"
    ]

    allied_keywords = [
        "support engineer", "technical support", "tech support", "application support", 
        "qa support", "it support", "trainee", "qa intern", "testing intern", "test intern",
        "junior developer", "junior software", "junior python", "graduate engineer", "data trainee"
    ]

    is_primary_qa = any(kw in title_lower for kw in primary_qa_keywords)
    is_ai_or_coding = any(kw in title_lower for kw in ai_and_programming_keywords)
    is_allied = any(kw in title_lower for kw in allied_keywords)

    # Exclude non-tech intern roles like marketing, hr, people ops, sales intern
    non_tech_flags = ["marketing", "recruitment", "human resources", "people ops", "talent", "electrical", "power electronics", "growth associate", "ux research", "copywriter"]
    if any(nt in title_lower for nt in non_tech_flags):
        return 0.0, "Rejected: Non-technical role"

    if not (is_primary_qa or is_ai_or_coding or is_allied):
        # Check description for strong AI / coding / QA context in tech intern roles
        if "intern" in title_lower or "trainee" in title_lower:
            if any(k in full_text for k in ["python", "artificial intelligence", "machine learning", "software engineering", "coding", "software developer"]):
                is_ai_or_coding = True
        
        if not is_ai_or_coding:
            if any(kw in description.lower() for kw in ["software testing", "manual testing", "qa testing", "test cases", "bug reporting"]):
                is_primary_qa = True
            else:
                return 0.0, "Rejected: Role is not QA, AI/Programming internship, or technical support role"

    # 3. Location / Work Mode Matching (STRICTLY 100% ONLINE / REMOTE / WFH ONLY)
    online_terms = [
        "remote", "work from home", "wfh", "online", "virtual", 
        "telecommute", "home-based", "anywhere", "worldwide", "remote / wfh"
    ]
    
    # Check for hard on-site / in-office exclusions
    strict_onsite_flags = [
        "on-site only", "onsite only", "work from office only", "wfo only", 
        "strictly in-office", "no remote", "not a remote", "in-person only"
    ]
    if any(flag in full_text for flag in strict_onsite_flags):
        return 0.0, "Rejected: Explicitly on-site / in-office role (User policy: 100% Online / Remote Only)"

    is_online_remote = any(term in full_text for term in online_terms)
    if not is_online_remote:
        return 0.0, "Rejected: Not an Online / Remote / WFH role (User policy: 100% Online / Remote Only)"

    # 4. Score Calculation (100% Online / Remote / WFH Guaranteed)
    score = 40.0
    reasons = []

    if is_primary_qa:
        score += 25.0
        reasons.append("🎯 Direct Software Tester / QA role")
    elif is_ai_or_coding:
        score += 25.0
        reasons.append("🤖 AI & Programming Internship role")
    else:
        score += 15.0
        reasons.append("🛠️ Allied Tech Support / Trainee role")

    # 100% Online / WFH Confirmation
    score += 25.0
    reasons.append("🌐 100% Online / Remote / WFH Opportunity")

    # Internship / Fresher boost
    if "intern" in title_lower or "internship" in title_lower:
        score += 10.0
        reasons.append("🎓 Preferred Internship opportunity")
    elif any(k in full_text for k in ["fresher", "trainee", "entry level", "junior", "graduate", "0-1", "0-2"]):
        score += 10.0
        reasons.append("Matches entry-level / fresher")

    # Skills matching
    skills_hit = [s for s in ["manual testing", "test cases", "jira", "postman", "bug", "python", "sql", "troubleshooting", "customer support"] if s in full_text]
    if skills_hit:
        score += 10.0
        reasons.append(f"Skills matched: {', '.join(skills_hit[:4])}")

    return min(score, 100.0), "; ".join(reasons)
