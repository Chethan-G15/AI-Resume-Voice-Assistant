from app.services.pdf_service import extract_text_from_pdf
from app.utils.section_parser import parse_resume_sections


pdf_path = "uploads/DarshanGR_Resume.pdf"

text = extract_text_from_pdf(pdf_path)

sections = parse_resume_sections(text)

for section_name, section_content in sections.items():

    print("\n" + "=" * 50)
    print(section_name.upper())
    print("=" * 50)

    print(section_content)