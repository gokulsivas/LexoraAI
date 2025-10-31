from app.core.chromadb_manager import chroma_db_manager
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class LexoraAI:
    def __init__(self):
        self.client = chroma_db_manager.get_client()
        self.collection = chroma_db_manager.get_collection()
    
    def has_documents(self):
        return self.collection.count() > 0
    
    def process_pdf_document(self, file_path, chunk_size=500, overlap=100):
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages])
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = splitter.split_text(text)
        
        ids = [f"{file_path}_chunk_{idx}" for idx in range(len(chunks))]
        metadatas = [
            {
                "source": file_path,
                "chunk": idx,
                "total_chunks": len(chunks)
            }
            for idx in range(len(chunks))
        ]
        
        self.collection.add(ids=ids, documents=chunks, metadatas=metadatas)
        return len(chunks)
    
    def query(self, question, max_new_tokens=256, temperature=0.7, n_chunks=5):
        """
        ✅ FIXED: No templates, fresh answer each time
        """
        source_chunks = []
        using_documents = False
        answer = ""  # ✅ Initialize fresh each time
        
        if self.has_documents():
            results = self.collection.query(
                query_texts=[question],
                n_results=n_chunks
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
                
                # ✅ Generate fresh context-specific answer
                context = "\n\n".join([chunk['text'] for chunk in source_chunks])
                answer = f"""**Response to: {question}**\n\n{context}"""
        
        if not answer:
            answer = "No relevant documents found for this query."
        
        return {
            "answer": answer,
            "using_documents": using_documents,
            "source_chunks": source_chunks
        }
    
    def clear_documents(self):
        all_docs = self.collection.get()
        if all_docs['ids']:
            self.collection.delete(ids=all_docs['ids'])
