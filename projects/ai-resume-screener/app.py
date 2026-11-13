"""
================================================================================
AI Resume Screener & ATS Match Microservice
Author: VARUN M S (Final Year BCA 2025 | AI & QA Developer)
Repository: https://github.com/varunms89/ai-resume-screener
Portfolio: https://varunms89.github.io
================================================================================

FastAPI microservice exposing REST API endpoints and interactive Swagger UI (/docs)
for automated ATS resume screening, semantic skill gap analysis, and fit evaluation.
"""

from typing import List, Optional, Dict, Any
from screener import evaluate_resume_against_job

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import RedirectResponse
    from pydantic import BaseModel, Field

    app = FastAPI(
        title="AI Resume & ATS Match Screener API",
        description="Production REST microservice for evaluating technical candidate fit against Job Descriptions. Engineered by Varun M S.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    class ScreenRequest(BaseModel):
        resume_text: str = Field(..., description="Full text of candidate resume or portfolio summary", example="VARUN M S - Final Year BCA 2025. Skills: Manual Testing, Test Cases, STLC, Postman, Python, SQL, Playwright.")
        job_description: str = Field(..., description="Full job description text with role requirements", example="Looking for QA Intern with Manual Testing, Test Cases, Postman API testing, and basic Python.")

    class ScreenResponse(BaseModel):
        candidate_name: str
        match_score: float
        total_required_skills_found: int
        matched_skills: List[str]
        missing_skills: List[str]
        recommendations: List[str]
        ats_status: str

    @app.get("/", include_in_schema=False)
    def root():
        """Redirects root visitor directly to interactive Swagger API documentation."""
        return RedirectResponse(url="/docs")

    @app.get("/health", tags=["System"])
    def health_check():
        """Health check probe endpoint for Kubernetes / cloud orchestrators."""
        return {
            "status": "HEALTHY",
            "service": "AI Resume & ATS Screener API",
            "author": "VARUN M S",
            "version": "1.0.0"
        }

    @app.post("/api/screen", response_model=ScreenResponse, tags=["Screening"])
    def screen_candidate(req: ScreenRequest):
        """
        Analyzes a resume against a target job description and returns an ATS score,
        matched technical competencies, and actionable recommendations.
        """
        if not req.resume_text.strip() or not req.job_description.strip():
            raise HTTPException(status_code=400, detail="Both resume_text and job_description must be provided.")

        result = evaluate_resume_against_job(req.resume_text, req.job_description)
        return result

except ImportError:
    # Fallback to standard lightweight WSGI/HTTP runner if FastAPI is not yet installed
    app = None

if __name__ == "__main__":
    try:
        import uvicorn
        print("🚀 Starting AI Resume Screener FastAPI on http://localhost:8000 ...")
        print("📖 Interactive Swagger Documentation live at: http://localhost:8000/docs")
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    except ImportError:
        print("💡 FastAPI or Uvicorn not installed. Run: pip install -r requirements.txt")
        print("Testing screening logic directly:")
        from screener import evaluate_resume_against_job
        res = evaluate_resume_against_job(
            "VARUN M S - BCA 2025. Skills: Manual Testing, Postman, Python, SQL.",
            "QA Tester Intern: Manual Testing, Postman, Python required."
        )
        import json
        print(json.dumps(res, indent=2))
