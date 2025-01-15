import io
import PyPDF2
import docx
from typing import BinaryIO

def parse_pdf(file: BinaryIO) -> str:
    """Parse PDF file and extract text."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def parse_docx(file: BinaryIO) -> str:
    """Parse DOCX file and extract text."""
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def parse_document(file: BinaryIO) -> str:
    """Parse uploaded document based on file type."""
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return parse_pdf(file)
    elif file_extension in ['docx', 'doc']:
        return parse_docx(file)
    else:
        raise ValueError("Unsupported file format")
