import chromadb

class ChromaDBManager:
    """Singleton ChromaDB manager - ensures only ONE instance across app"""
    
    _instance = None
    _client = None
    _collection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self, db_path="./chromadb_data", collection_name="crpc_chapters_chunked"):
        """Initialize ChromaDB client and collection - call once in main.py"""
        if self._client is None:
            self._client = chromadb.PersistentClient(path=db_path)
            self._collection = self._client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        return self._client, self._collection
    
    def get_client(self):
        """Get ChromaDB client"""
        if self._client is None:
            self.initialize()
        return self._client
    
    def get_collection(self):
        """Get ChromaDB collection"""
        if self._collection is None:
            self.initialize()
        return self._collection


# Global instance
chroma_db_manager = ChromaDBManager()
