import chromadb
from pathlib import Path
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def upload_pdfs_chunked_to_chromadb(pdf_folder, collection_name="crpc_chapters_chunked", chunk_size=1000):
    """Upload PDFs to ChromaDB with persistent storage"""
    
    # ✅ PERSISTENT CLIENT - saves data to ./chromadb_data folder
    client = chromadb.PersistentClient(path="./chromadb_data")
    
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    
    pdf_files = sorted(Path(pdf_folder).glob("*.pdf"))
    doc_count = 0
    
    for pdf_file in pdf_files:
        try:
            reader = PdfReader(str(pdf_file))
            text = "\n".join([page.extract_text() for page in reader.pages])
            chunks = splitter.split_text(text)
            
            for chunk_idx, chunk in enumerate(chunks):
                doc_id = f"{pdf_file.stem}_chunk_{chunk_idx}"
                collection.add(
                    ids=[doc_id],
                    documents=[chunk],
                    metadatas=[{
                        "filename": pdf_file.name,
                        "chunk_id": chunk_idx,
                        "total_chunks": len(chunks),
                        "source": "CrPC-1973"
                    }]
                )
                doc_count += 1
            
            print(f"✓ {pdf_file.name}: {len(chunks)} chunks uploaded")
        except Exception as e:
            print(f"✗ Error: {pdf_file.name} - {e}")
    
    print(f"\n✓ Total chunks uploaded: {doc_count}")
    return collection


if __name__ == "__main__":
    pdf_path = r"C:\Users\gokul\Downloads\booksss\CrPC"
    print("Starting ChromaDB upload with persistent storage...\n")
    collection = upload_pdfs_chunked_to_chromadb(pdf_path)
    print("Upload complete! Data saved to ./chromadb_data/")
