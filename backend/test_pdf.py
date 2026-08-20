from app.services.pdf_service import extract_text_from_pdf


pdf_path = "uploads/Chethan_Resume.pdf"

text = extract_text_from_pdf(pdf_path)

print(text)