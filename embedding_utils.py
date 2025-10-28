from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def embed_text(text_chunks):
    #Convert list of text chunks into vector embeddings
    embeddings = model.encode(text_chunks, show_progress_bar=True)
    return embeddings

if __name__ == "__main__":
    sample_chunks = [
        "This is the first legal document chunk about contract obligations.",
        "Another chunk discussing terms related to inspection and compliance.",
        "Final sample chunk mentioning licenses and intellectual property rights."
    ]
    embeddings = embed_text(sample_chunks)
    print("Embeddings shape:", embeddings.shape)
    print("First embedding vector (truncated):", embeddings[0][:10])
