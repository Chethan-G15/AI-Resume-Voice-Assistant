from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from app.services.whisper_service import transcribe_audio
from app.services.ollama_service import understand_query
from app.repositories.resume_repository import get_resume_by_candidate


router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)


VOICE_UPLOAD_DIR = Path("voice_uploads")
VOICE_UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/query")
async def voice_query(file: UploadFile = File(...)):

    # 1. Save audio temporarily
    file_path = VOICE_UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Convert speech to text
    try:
        text_query = transcribe_audio(str(file_path))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not transcribe the audio."
        )

    # 3. Check empty transcription
    if not text_query.strip():
        return {
            "answer": "I could not hear your question clearly."
        }

    # 4. Ollama understands the text query
    try:
        result = understand_query(text_query)
    except Exception:
        return {
            "answer": "I could not understand your question."
        }

    candidate_name = result.get("candidate_name")
    requested_section = result.get("requested_section")

    # 5. Validate Ollama result
    if not candidate_name or not requested_section:
        return {
            "answer": "No such information is available."
        }

    # 6. Allowed sections
    section_index = {
        "career_objective": 3,
        "skills": 4,
        "education": 5,
        "experience": 6,
        "projects": 7,
        "certifications": 8
    }

    if requested_section not in section_index:
        return {
            "answer": "No such information is available."
        }

    # 7. Retrieve actual resume information from SQLite
    resume = get_resume_by_candidate(candidate_name)

    if resume is None:
        return {
            "answer": f"I could not find a resume for {candidate_name}."
        }

    # 8. Get actual information from SQLite
    answer = resume[section_index[requested_section]]

    # 9. Validate database information
    if not answer or not answer.strip():
        return {
            "answer": (
                f"No {requested_section.replace('_', ' ')} "
                f"information is available for {resume[1]}."
            )
        }

    # 10. Return actual database information
    return {
        "voice_text": text_query,
        "candidate_name": resume[1],
        "requested_section": requested_section,
        "answer": answer
    }