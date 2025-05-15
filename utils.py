import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from all pages of a PDF and returns it as a single string.
    :param pdf_path: Path to the PDF file
    :return: Concatenated text from all pages
    """
    text = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text.append(page.get_text())
    return '\n'.join(text) 