import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import os

# 🔧 Set Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔧 Set Poppler path (Windows only)
POPPLER_PATH = r"C:\poppler\Library\bin"


def extract_text(pdf_path):
    """
    Extract text from PDF.
    If normal extraction fails, fallback to OCR.
    """

    text = ""

    # 🟢 STEP 1: Try normal text extraction
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        pass

    # 🟡 STEP 2: If no text found → OCR
    if len(text.strip()) < 50:
        print("⚠️ No readable text found. Using OCR...")

        images = convert_from_path(
            pdf_path,
            poppler_path=POPPLER_PATH
        )

        for img in images:
            ocr_text = pytesseract.image_to_string(img)
            text += ocr_text + "\n"

    return text