from fastapi import APIRouter, HTTPException

from app.repositories.resume_repository import get_resume_by_candidate


router = APIRouter(
    prefix="/resumes",
    tags=["Resume Retrieval"]
)


@router.get("/{candidate_name}")
def get_resume(candidate_name: str):

    row = get_resume_by_candidate(candidate_name)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Candidate '{candidate_name}' not found."
        )

    return {
        "id": row[0],
        "candidate_name": row[1],
        "filename": row[2],
        "career_objective": row[3],
        "skills": row[4],
        "education": row[5],
        "experience": row[6],
        "projects": row[7],
        "certifications": row[8]
    }