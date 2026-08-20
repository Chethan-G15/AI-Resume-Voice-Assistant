from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from app.utils.section_parser import (
    parse_resume_sections,
    extract_candidate_name,
    extract_email,
    extract_phone
)
from app.database.database import create_tables
from app.repositories.resume_repository import insert_resume


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


# --------------------------------------------------
# Upload directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Make sure database table exists
# --------------------------------------------------

create_tables()

# upload resume here it will accept the pdf
@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was selected."
        )

    # Check for .pdf extention
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

# save pdf inside the uploads folder
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

# extract all text from pdf from uploads folder
    text = extract_text_from_pdf(str(file_path))

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the PDF."
        )

# firts it will extract only name from pdf
    candidate_name = extract_candidate_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

# all inside the pdf will going extract

    sections = parse_resume_sections(text)

# save all extracted data in database in below format 

    resume_id = insert_resume(
        candidate_name=candidate_name,
         email=email,
         phone=phone,
        filename=file.filename,
        career_objective=sections["career_objective"],
        skills=sections["skills"],
        education=sections["education"],
        experience=sections["experience"],
        projects=sections["projects"],
        certifications=sections["certifications"]
    )

    # --------------------------------------------------
    # 6. Return response
    # --------------------------------------------------

    return {
        "message": "Resume uploaded and processed successfully",
        "resume_id": resume_id,
        "candidate_name": candidate_name,
        "email": email,
        "phone": phone,
        "filename": file.filename
    }