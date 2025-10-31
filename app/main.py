from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.chromadb_manager import chroma_db_manager
from app.routers import api


app = FastAPI(title="LexoraAI", version="1.0.0")

# ✅ Initialize the SINGLE ChromaDB instance
client, collection = chroma_db_manager.initialize(
    db_path="./chromadb_data",
    collection_name="crpc_chapters_chunked"
)

# Store in app state for access in routes
app.state.chroma_db_manager = chroma_db_manager


# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api.router, prefix="/api", tags=["LexoraAI"])


@app.get("/")
def health_check():
    try:
        collection = chroma_db_manager.get_collection()
        return {
            "status": "LexoraAI running",
            "chromadb_documents": collection.count(),
            "chromadb_path": "./chromadb_data"
        }
    except Exception as e:
        return {
            "status": "LexoraAI running",
            "chromadb_error": str(e)
        }
