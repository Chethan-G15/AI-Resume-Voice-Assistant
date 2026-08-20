from app.services.pdf_service import extract_text_from_pdf
from app.utils.section_parser import (
    parse_resume_sections,
    extract_candidate_name
)
from app.database.database import create_tables
from app.repositories.resume_repository import insert_resume


# --------------------------------------------------
# 1. Create database table
# --------------------------------------------------

create_tables()


# --------------------------------------------------
# 2. PDF path
# --------------------------------------------------

pdf_path = "uploads/Chethan_Resume.pdf"


# --------------------------------------------------
# 3. Extract PDF text
# --------------------------------------------------

text = extract_text_from_pdf(pdf_path)


# --------------------------------------------------
# 4. Extract candidate name
# --------------------------------------------------

candidate_name = extract_candidate_name(text)


# --------------------------------------------------
# 5. Parse resume sections
# --------------------------------------------------

sections = parse_resume_sections(text)


# --------------------------------------------------
# 6. Save into database
# --------------------------------------------------

resume_id = insert_resume(
    candidate_name=candidate_name,
    filename=pdf_path.split("/")[-1],
    career_objective=sections["career_objective"],
    skills=sections["skills"],
    education=sections["education"],
    experience=sections["experience"],
    projects=sections["projects"],
    certifications=sections["certifications"]
)


print("Resume processed successfully.")
print(f"Candidate: {candidate_name}")
print(f"Resume ID: {resume_id}")