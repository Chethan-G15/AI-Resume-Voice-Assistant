import fitz


def extract_text_from_pdf(file_path: str) -> str:
# extract text from all pages of pdf


# this is like file handling open pdf and read the data from there
# if resume is more than one also this PYMuPDF
    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text