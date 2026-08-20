from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ollama_service import understand_query
from app.repositories.resume_repository import get_resume_by_candidate


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


class QueryRequest(BaseModel):
    query: str


@router.post("/")
def query_resume(request: QueryRequest):

    # 1. Check empty query
    if not request.query.strip():
        return {
            "answer": "Please ask a question about a candidate's resume."
        }

    # 2. Ollama understands the query
    try:
        result = understand_query(request.query)
    except Exception:
        return {
            "answer": "I could not understand your question. Please ask something different."
        }

    candidate_name = result.get("candidate_name")
    requested_section = result.get("requested_section")

    # 3. Validate Ollama result
    if not candidate_name or not requested_section:
        return {
            "answer": "No such information is available. Please ask something different."
        }

    # 4. Allowed resume sections
    section_index = {
        "career_objective": 5,
        "skills": 6,
        "education": 7,
        "experience": 8,
        "projects": 9,
        "certifications": 10,
        "email": 2,
        "phone": 3
    }

    # 5. Check requested section
    if requested_section not in section_index:
        return {
            "answer": "No such information is available. Please ask something different."
        }

    # 6. Find candidate in SQLite
    resume = get_resume_by_candidate(candidate_name)

    if resume is None:
        return {
            "answer": f"I could not find a resume for {candidate_name}. Please ask about another candidate."
        }

    # 7. Get actual information from SQLite
    answer = resume[section_index[requested_section]]

    # 8. Check whether information exists
    if not answer or not answer.strip():
        return {
            "answer": f"No {requested_section.replace('_', ' ')} information is available for {resume[1]}."
        }

    # 9. Return actual database information
    return {
        "candidate_name": resume[1],
        "requested_section": requested_section,
        "answer": answer
    }