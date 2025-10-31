from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
import shutil
import os
from app.core.lexora import LexoraAI
from app.core.chromadb_manager import chroma_db_manager
import warnings

warnings.filterwarnings("ignore")

router = APIRouter()
lexora = LexoraAI()  # ✅ Uses singleton ChromaDB


class QueryRequest(BaseModel):
    question: str
    max_new_tokens: int = 256
    temperature: float = 0.7
    n_chunks: int = 5


class QueryResponse(BaseModel):
    answer: str
    using_documents: bool
    source_chunks: list


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process PDF document"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    try:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        chunks_count = lexora.process_pdf_document(
            file_path,
            chunk_size=500,
            overlap=100
        )
        
        os.remove(file_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_stored": chunks_count
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the model with optional document context"""
    response = lexora.query(
        question=request.question,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature,
        n_chunks=request.n_chunks
    )
    return response


@router.get("/documents/count")
async def get_document_count():
    """Get count of stored document chunks"""
    try:
        collection = chroma_db_manager.get_collection()
        return {"total_chunks": collection.count()}
    except Exception as e:
        return {"total_chunks": 0, "error": str(e)}


@router.post("/documents/clear")
async def clear_documents():
    """Clear all stored documents"""
    try:
        lexora.clear_documents()
        return {"status": "success", "message": "All documents cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/documents/list")
async def list_documents(limit: int = 50):
    """List all stored chunks"""
    try:
        collection = chroma_db_manager.get_collection()
        doc_count = collection.count()
        
        if doc_count == 0:
            return {"total_chunks": 0, "documents": []}
        
        all_docs = collection.get(include=["documents", "metadatas"])
        
        documents = []
        for i, (doc_id, document, metadata) in enumerate(zip(
            all_docs['ids'],
            all_docs['documents'],
            all_docs['metadatas']
        )):
            documents.append({
                "chunk_id": doc_id,
                "source": metadata.get("source", "unknown"),
                "chunk_number": metadata.get("chunk", 0),
                "text_preview": document[:200] + "..." if len(document) > 200 else document,
                "full_text_length": len(document)
            })
            
            if i >= limit - 1:
                break
        
        return {
            "total_chunks": doc_count,
            "showing": min(limit, len(documents)),
            "documents": documents
        }
    except Exception as e:
        return {"error": str(e)}
