# backend/utils/pdf_tools.py
"""
Utility functions for extracting text from PDF and DOCX files.
"""

import os
from pdfminer.high_level import extract_text as extract_pdf_text
import docx

def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from a PDF or DOCX file.

    Args:
        file_path (str): Path to the uploaded file

    Returns:
        str: Extracted text as plain string
    """
    filename = file_path.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file_path)

    elif filename.endswith(".docx") or filename.endswith(".doc"):
        try:
            doc = docx.Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except Exception as e:
            return f"[Error extracting DOCX text: {str(e)}]"

    else:
        return "[Unsupported file type]"
