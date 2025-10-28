import chromadb
from sentence_transformers import SentenceTransformer

# Create client with default settings (no arguments)
client = chromadb.Client()

# Create or get the collection
collection = client.get_or_create_collection("legal_doc_chunks")

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def embed_text(text_chunks):
    return model.encode(text_chunks).tolist()

def store_chunks(chunks):
    embeddings = embed_text(chunks)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB.")


    print(f"Stored {len(chunks)} chunks in ChromaDB.")

def query_chroma(query, top_k=3):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results

if __name__ == "__main__":
    sample_chunks = [
        "This is a sample legal document chunk about agreements.",
        "This chunk discusses inspection clauses and responsibilities.",
        "This chunk covers licensing rights and intellectual property."
    ]
    store_chunks(sample_chunks)

    q = "What are the responsibilities for inspection?"
    res = query_chroma(q)
    print("Top relevant chunks for query:")
    for doc in res['documents'][0]:
        print("-", doc)
