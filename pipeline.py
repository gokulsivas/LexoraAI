import os
from document_ingestion import ingest_document
from sentence_transformers import SentenceTransformer
import chromadb
from transformers import AutoTokenizer, Gemma3ForCausalLM
import torch
from safetensors.torch import load_file


# Load your fine-tuned Gemma generative model
model_name = "google/gemma-3-1b-it"  # Base model from Hugging Face
adapter_path = r"F:\GenAI\finetuned-gemma\adapter_model.safetensors"


# Load tokenizer from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_name)


# Load base model from Hugging Face
generative_model = Gemma3ForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16
)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
generative_model.to(device)


# Load and apply your fine-tuned adapter weights on top of base model using safetensors
adapter_weights = load_file(adapter_path, device="cpu")
generative_model.load_state_dict(adapter_weights, strict=False)


# Set device (GPU if available)
generative_model.to(device)
generative_model.eval()


# Initialize Chroma client and collection
client = chromadb.Client()
collection = client.get_or_create_collection("legal_doc_chunks")


# Load embedding model with different variable name to avoid conflict
embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')


def embed_text(text_chunks):
    return embedding_model.encode(text_chunks).tolist()


def process_and_store(file_path):
    chunks = ingest_document(file_path)
    print(f"Ingested and chunked into {len(chunks)} chunks.")

    embeddings = embed_text(chunks)
    ids = [f"{os.path.basename(file_path)}_chunk_{i}" for i in range(len(chunks))]
    collection.add(ids=ids, documents=chunks, embeddings=embeddings)
    print(f"Stored {len(chunks)} chunks from {file_path}.")


def query_documents(query, top_k=5):
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results['documents'][0]


def generate_text(prompt, max_length=200):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(device)
    with torch.inference_mode():
        outputs = generative_model.generate(**inputs, max_new_tokens=max_length)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def summarize_chunks(chunks):
    combined_text = " ".join(chunks)[:3000]
    prompt = f"Summarize the following text:\n{combined_text}"
    return generate_text(prompt)


def answer_question(question, chunks):
    combined_text = " ".join(chunks)[:3000]
    prompt = f"Based on the following text:\n{combined_text}\nAnswer this question:\n{question}"
    return generate_text(prompt)


if __name__ == "__main__":
    sample_pdf = r"D:\GOKUL-UG\VIT\Projects\AI\LexoraAI\samples\SampleContract-Shuttle.pdf"
    process_and_store(sample_pdf)

    # Test querying relevant chunks with expanded top_k
    results = query_documents("What happens if the consultant wants to subcontract some of the work?", top_k=10)
    
    if results:
        print("Summary of relevant chunks:")
        print(summarize_chunks(results))

        print("\nAnswer to your question:")
        answer = answer_question("What is the process for resolving disputes?", results)
        print(answer)
    else:
        print("No relevant chunks found for the query.")
