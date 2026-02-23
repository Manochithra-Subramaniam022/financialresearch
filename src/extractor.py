import pdfplumber

def extract_text(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text(layout=True) or ""
    return all_text