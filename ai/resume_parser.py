import os
import pdfplumber


def extract_text_from_pdf(pdf_path):

    # Check that the file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"Resume file not found: {pdf_path}"
        )

    # Check that the file is not empty
    file_size = os.path.getsize(pdf_path)

    if file_size == 0:
        raise ValueError(
            "The uploaded PDF file is empty."
        )

    # Check PDF file signature
    with open(pdf_path, "rb") as f:
        header = f.read(5)

    if header != b"%PDF-":
        raise ValueError(
            "The uploaded file is not a valid PDF. "
            "Please upload a genuine PDF resume."
        )

    # Extract text
    text = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:

        raise ValueError(
            "The PDF appears to be corrupted or unreadable. "
            "Please open the PDF on your computer and save it again as a new PDF."
        ) from e

    # Make sure some text was extracted
    if not text.strip():

        raise ValueError(
            "No readable text was found in the PDF. "
            "If your resume is scanned/image-based, OCR may be required."
        )

    return text