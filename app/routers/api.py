from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import shutil
import os
from app.core.lexora import LexoraAI
from app.core.chromadb_manager import chroma_db_manager
import warnings
import requests
import json

warnings.filterwarnings("ignore")

router = APIRouter()
lexora = LexoraAI()


class QueryRequest(BaseModel):
    question: str
    max_new_tokens: int = 256
    temperature: float = 0.7
    n_chunks: int = 5
    doc_type: Optional[str] = None  # ✅ FIXED: Optional, not required


class QueryResponse(BaseModel):
    answer: str
    using_documents: bool
    source_chunks: list


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), doc_type: str = "general"):
    """Upload and process PDF document with document type"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    try:
        print(f"\n🔍 UPLOAD DEBUG:")
        print(f"   Received doc_type parameter: '{doc_type}'")
        print(f"   File: {file.filename}")
        
        file_path = f"temp_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"   Calling process_pdf_document with doc_type='{doc_type}'")
        
        chunks_count = lexora.process_pdf_document(
            file_path,
            doc_type=doc_type
        )
        
        print(f"   Stored {chunks_count} chunks")
        
        os.remove(file_path)
        
        response = {
            "status": "success",
            "filename": file.filename,
            "doc_type": doc_type,
            "chunks_stored": chunks_count
        }
        
        print(f"   Response: {response}\n")
        return response
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}\n")
        return {"status": "error", "message": str(e)}


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the model - searches ALL documents"""
    try:
        print(f"\n🔍 QUERY REQUEST:")
        print(f"   Question: {request.question}")
        print(f"   N Chunks: {request.n_chunks}")
        
        # ✅ ALWAYS search all documents (doc_type = None)
        response = lexora.query(
            question=request.question,
            doc_type=None,
            n_chunks=request.n_chunks
        )
        
        print(f"   Documents found: {response.get('using_documents')}")
        
        # If documents found, summarize them
        if response.get('using_documents') and response.get('answer'):
            print(f"   🔄 Calling Ollama to summarize...")
            
            summary_response = await summarize_text({
                "text": response.get('answer', ''),
                "question": request.question
            })
            
            response['answer'] = summary_response.get('summary', response.get('answer'))
            print(f"   ✅ Answer summarized!")
        
        return response
    except Exception as e:
        print(f"❌ Query error: {e}")
        return {
            "answer": f"Error: {str(e)}",
            "using_documents": False,
            "source_chunks": []
        }


@router.get("/documents/count")
async def get_document_count(doc_type: Optional[str] = None):
    """Get count of stored document chunks"""
    try:
        collection = chroma_db_manager.get_collection()
        
        if doc_type:
            all_docs = collection.get(where={"doc_type": {"$eq": doc_type}})
            count = len(all_docs['ids']) if all_docs['ids'] else 0
        else:
            count = collection.count()
        
        return {"total_chunks": count}
    except Exception as e:
        return {"total_chunks": 0, "error": str(e)}


@router.post("/documents/clear")
async def clear_documents(doc_type: Optional[str] = None):
    """Clear all stored documents, or only specific doc_type"""
    try:
        collection = chroma_db_manager.get_collection()
        
        if doc_type:
            all_docs = collection.get(where={"doc_type": {"$eq": doc_type}})
            if all_docs['ids']:
                collection.delete(ids=all_docs['ids'])
            return {
                "status": "success",
                "message": f"All '{doc_type}' documents cleared"
            }
        else:
            lexora.clear_documents()
            return {"status": "success", "message": "All documents cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/documents/list")
async def list_documents(limit: int = 50, doc_type: Optional[str] = None):
    """List all stored chunks"""
    try:
        collection = chroma_db_manager.get_collection()
        
        if doc_type:
            all_docs = collection.get(
                where={"doc_type": {"$eq": doc_type}},
                include=["documents", "metadatas"]
            )
        else:
            all_docs = collection.get(include=["documents", "metadatas"])
        
        doc_count = len(all_docs['ids']) if all_docs['ids'] else 0
        
        if doc_count == 0:
            return {"total_chunks": 0, "documents": []}
        
        documents = []
        for i, (doc_id, document, metadata) in enumerate(zip(
            all_docs['ids'],
            all_docs['documents'],
            all_docs['metadatas']
        )):
            documents.append({
                "chunk_id": doc_id,
                "source": metadata.get("source", "unknown"),
                "doc_type": metadata.get("doc_type", "general"),
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


@router.get("/documents/types")
async def list_document_types():
    """List all unique document types in collection"""
    try:
        collection = chroma_db_manager.get_collection()
        
        print(f"\n--- list_document_types called ---")
        print(f"  Total docs in collection: {collection.count()}")
        
        all_docs = collection.get(include=["metadatas"])
        
        doc_types = set()
        for idx, metadata in enumerate(all_docs['metadatas']):
            doc_type = metadata.get("doc_type", "general")
            doc_types.add(doc_type)
        
        print(f"  Final doc_types: {doc_types}")
        print(f"--- end list_document_types ---\n")
        
        return {
            "document_types": list(doc_types),
            "count": len(doc_types)
        }
    except Exception as e:
        print(f"ERROR in list_document_types: {e}")
        return {"error": str(e)}


@router.post("/summarize")
async def summarize_text(request: dict):
    """Summarize using FREE local Ollama model (Mistral)"""
    raw_text = request.get("text", "")
    question = request.get("question", "")
    
    if not raw_text or len(raw_text) < 50:
        return {"summary": "Information not found in provided documents."}
    
    raw_text = raw_text[:3000]
    
    prompt = f"""You are a strict legal document analyzer. Do NOT make up information.

User Question: "{question}"

Legal Text:
{raw_text}

CRITICAL RULES:
1. ONLY use information explicitly stated in the legal text above
2. If the question cannot be answered from the text, respond EXACTLY with: "This information is not available in the provided documents."
3. Do NOT use general knowledge, do NOT infer, do NOT guess
4. Do NOT mention government ministers, cabinet positions, or political offices unless explicitly in the text
5. Be concise and direct
6. Use only facts from the text provided

Answer the question now. If it's not in the text, say so:"""

    try:
        print(f"\n🔄 SUMMARIZE DEBUG:")
        print(f"   Question: {question}")
        print(f"   Raw text length: {len(raw_text)}")
        print(f"   Calling Ollama...")
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'mistral',
                'prompt': prompt,
                'stream': False,
                'temperature': 0.1  # ← LOWER temperature = less hallucination
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result.get('response', '').strip()
            
            print(f"   ✅ Ollama returned {len(summary)} chars")
            
            if not summary or "Error" in summary:
                print(f"   ⚠️ Ollama returned empty/error")
                return {"summary": "Unable to process your question."}
            
            return {"summary": summary}
        else:
            print(f"   ❌ Ollama HTTP Error: {response.status_code}")
            return {"summary": "Error processing request."}
            
    except requests.exceptions.Timeout:
        print(f"   ❌ Ollama TIMEOUT")
        return {"summary": "Request timed out. Please try again."}
    except Exception as e:
        print(f"   ❌ Ollama error: {e}")
        return {"summary": "Error processing request."}
