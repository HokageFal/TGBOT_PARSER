from PyPDF2 import PdfReader
from docx import Document
from parser_bot.services.regex import extract_section


def read_pdf(file_path: str) -> str:
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    return extract_section(text, "Навыки", "Резюме обновлено")

def read_docx(file_path: str) -> str:
    doc = Document(file_path)
    full_text = []

    for para in doc.paragraphs:
        full_text.append(para.text)

    return '\n'.join(full_text)
