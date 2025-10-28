import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Define regex patterns to detect legal headings and numbered clauses common in Indian legal docs
LEGAL_HEADING_PATTERNS = [
    r'^(Section|SECTION|S\.|Sec\.)\s*\d+(\.\d+)*',  # e.g. Section 1, Section 2.3 etc.
    r'^\d+\.\d+(\.\d+)*',                         # e.g. 1.1, 2.3.4 subsections
    r'^(Clause|CLAUSE)\s*\d+(\.\d+)*',            # Clauses numbered
    r'^(Article|ARTICLE)\s*\d+',                   # Articles numbering
]

def is_legal_heading(text_line):
    """Detect if a line matches any legal heading patterns"""
    for pattern in LEGAL_HEADING_PATTERNS:
        if re.match(pattern, text_line.strip()):
            return True
    return False

def custom_split_text(text, chunk_size=1000, chunk_overlap=100):
    """Split text into chunks respecting custom legal heading breakpoints"""
    # First filter and tag lines that are legal headings
    lines = text.splitlines()
    
    split_points = []
    for i, line in enumerate(lines):
        if is_legal_heading(line):
            split_points.append(i)

    # If no split points detected, fallback to RecursiveCharacterTextSplitter (RCTS)
    if not split_points:
        rcts = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return rcts.split_text(text)

    # Otherwise split text by ranges defined by detected headings
    chunks = []
    for i in range(len(split_points)):
        start = split_points[i]
        end = split_points[i+1] if i+1 < len(split_points) else len(lines)
        chunk_lines = lines[start:end]
        
        chunk_text = "\n".join(chunk_lines).strip()
        # Optionally further split if chunk too long using RecursiveCharacterTextSplitter
        if len(chunk_text) > chunk_size:
            rcts = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            sub_chunks = rcts.split_text(chunk_text)
            chunks.extend(sub_chunks)
        else:
            chunks.append(chunk_text)
    return chunks

# Example use
if __name__ == "__main__":
    with open(r"D:\GOKUL-UG\VIT\Projects\AI\LexoraAI\samples\cleaned_legal_text.txt", "r", encoding="utf-8") as f:
        text = f.read()
    chunks = custom_split_text(text, chunk_size=1000, chunk_overlap=200)
    print(f"Total Chunks: {len(chunks)}")
    for idx, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {idx+1} preview:\n{chunk[:500]}...\n")
