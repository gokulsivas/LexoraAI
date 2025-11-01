from app.core.chromadb_manager import chroma_db_manager
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class LexoraAI:
    def __init__(self):
        """Initialize LexoraAI using the SINGLE ChromaDB instance"""
        self.client = chroma_db_manager.get_client()
        self.collection = chroma_db_manager.get_collection()
    
    def has_documents(self):
        """Check if collection has documents"""
        return self.collection.count() > 0
    
    def process_pdf_document(self, file_path, doc_type="general", chunk_size=500, overlap=100):
        """Process and store PDF chunks with doc_type metadata - FIXED"""
        print(f"\n--- process_pdf_document called ---")
        print(f"  file_path: {file_path}")
        print(f"  doc_type: '{doc_type}'")
        
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages])
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = splitter.split_text(text)
        print(f"  Created {len(chunks)} chunks")
        
        ids = [f"{file_path}_chunk_{idx}" for idx in range(len(chunks))]
        metadatas = [
            {
                "source": file_path,
                "doc_type": doc_type,
                "chunk": idx,
                "total_chunks": len(chunks)
            }
            for idx in range(len(chunks))
        ]
        
        print(f"  First metadata: {metadatas[0]}")
        
        self.collection.add(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )
        
        print(f"  Stored in ChromaDB")
        print(f"--- end process_pdf_document ---\n")
        
        return len(chunks)
    
    def query(self, question, doc_type=None, n_chunks=5):
        """Query with optional doc_type metadata filter"""
        source_chunks = []
        using_documents = False
        answer = ""
        
        if self.has_documents():
            where_filter = None
            if doc_type:
                where_filter = {"doc_type": {"$eq": doc_type}}
            
            try:
                results = self.collection.query(
                    query_texts=[question],
                    n_results=n_chunks,
                    where=where_filter
                )
                
                if results['documents'] and len(results['documents'][0]) > 0:
                    using_documents = True
                    source_chunks = [
                        {
                            "text": results['documents'][0][i],
                            "metadata": results['metadatas'][0][i],
                            "distance": float(results['distances'][0][i])
                        }
                        for i in range(len(results['documents'][0]))
                    ]
            except Exception as e:
                print(f"Query error: {e}")
                using_documents = False
        
        if using_documents:
            context = "\n".join([chunk['text'] for chunk in source_chunks])
            answer = f"**Response to: {question}**\n\n{context}"
        else:
            answer = "No relevant documents found."
        
        return {
            "answer": answer,
            "using_documents": using_documents,
            "source_chunks": source_chunks
        }
    
    def clear_documents(self):
        """Clear all documents"""
        all_docs = self.collection.get()
        if all_docs['ids']:
            self.collection.delete(ids=all_docs['ids'])
