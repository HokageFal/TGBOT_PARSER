from PyPDF2 import PdfReader
from docx import Document
from parser_bot.services.regex import extract_section
import win32com.client

def read_pdf(file_path: str) -> str:
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    return text

def read_docx(file_path: str) -> str:
    doc = Document(file_path)
    full_text = []

    for para in doc.paragraphs:
        full_text.append(para.text)

    return '\n'.join(full_text)

def read_doc(file_path: str) -> str:
    word = win32com.client.Dispatch("Word.Application")
    doc = word.Documents.Open(file_path)
    text = doc.Content.Text
    doc.Close()
    word.Quit()
    return text
