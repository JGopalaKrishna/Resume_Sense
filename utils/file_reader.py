import fitz  # PyMuPDF
import docx

def extract_text_from_files(files):
    texts = []
    for file in files:
        if file.type == "application/pdf":
            texts.append(extract_text_from_pdf(file))
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            texts.append(extract_text_from_docx(file))
        else:
            texts.append("")
    return texts

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file):
    text = ""
    doc = docx.Document(file)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text
