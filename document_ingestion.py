import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Tesseract path config (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

LEGAL_HEADING_PATTERNS = [
    r'^(Section|SECTION|S\.|Sec\.)\s*\d+(\.\d+)*',
    r'^\d+\.\d+(\.\d+)*',
    r'^(Clause|CLAUSE)\s*\d+(\.\d+)*',
    r'^(Article|ARTICLE)\s*\d+',
]

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()
    return text

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def clean_text(text):
    text = re.sub(r"Page \d+ of \d+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n\s*\n", "\n", text)  # remove multiple empty lines
    text = re.sub(r"[ \t]+", " ", text)   # multiple spaces/tabs to one
    return text.strip()

def is_legal_heading(text_line):
    for pattern in LEGAL_HEADING_PATTERNS:
        if re.match(pattern, text_line.strip()):
            return True
    return False

def custom_split_text(text, chunk_size=1000, chunk_overlap=100):
    lines = text.splitlines()
    
    split_points = [i for i, line in enumerate(lines) if is_legal_heading(line)]
    
    if not split_points:
        rcts = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return rcts.split_text(text)

    chunks = []
    for i in range(len(split_points)):
        start = split_points[i]
        end = split_points[i+1] if i+1 < len(split_points) else len(lines)
        chunk_lines = lines[start:end]
        chunk_text = "\n".join(chunk_lines).strip()
        
        if len(chunk_text) > chunk_size:
            rcts = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chunks.extend(rcts.split_text(chunk_text))
        else:
            chunks.append(chunk_text)
    return chunks

def ingest_document(file_path, chunk_size=1000, chunk_overlap=100):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
        text = extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    cleaned_text = clean_text(text)
    chunks = custom_split_text(cleaned_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    return chunks

# Example usage
if __name__ == "__main__":
    sample_pdf = "D:\GOKUL-UG\VIT\Projects\AI\LexoraAI\samples\SampleContract-Shuttle.pdf"
    chunks = ingest_document(sample_pdf)
    print(f"Extracted {len(chunks)} chunks")
    for i, c in enumerate(chunks[:3]):
        print(f"\n--- Chunk {i+1} preview ---\n{c[:500]}...\n")
