<div align="center">
   
# LexoraAI

**Privacy-first AI for legal documents - runs entirely on your machine.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org)
[![Ollama](https://img.shields.io/badge/Ollama-Llama3-black?style=flat)](https://ollama.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

LexoraAI is a local, offline-first AI chatbot that lets you query legal PDFs using Retrieval-Augmented Generation (RAG). Upload a judgment or contract, ask questions in plain English, and get context-aware answers which is powered by Llama3 via Ollama, with zero cloud dependency.

<img width="3656" height="2011" alt="image" src="https://github.com/user-attachments/assets/2bbb4ef0-c4b1-41e9-a67f-cc3b98eccc31" />

<img width="3789" height="2087" alt="image" src="https://github.com/user-attachments/assets/5679ebdc-a31d-4986-bdb0-849a76626049" />


---

## Features

- **Secure Authentication** - JWT-based sign-up and login
- **PDF Upload & RAG Pipeline** - Documents are chunked, embedded, and stored in ChromaDB for semantic retrieval
- **Local LLM Inference** - Queries processed by Llama3 via Ollama; no data leaves your machine
- **Real-time Streaming Replies** - Responses stream token-by-token in the chat UI
- **Polished UI** - Auto-scroll, animated backgrounds, file management, and chat history

---

## Architecture

<img width="830" height="494" alt="lexoraai_system_architecture_dark" src="https://github.com/user-attachments/assets/2139934a-17e5-451c-93f9-0137ebea5ecb" />


---

## Tech Stack

| Layer      | Technology                                          |
|------------|-----------------------------------------------------|
| Frontend   | React 18, React Router, Tailwind CSS, Lucide React  |
| Backend    | FastAPI, SQLAlchemy (SQLite), Pydantic, Uvicorn      |
| AI / RAG   | Ollama (Llama3), Sentence Transformers, ChromaDB    |
| Auth       | JWT (JSON Web Tokens)                               |

---

## Project Structure
```
LexoraAI/
├── app/                 # FastAPI app modules
├── lexora-ui/           # React frontend
│   └── src/
│       ├── App.jsx
│       ├── Chat.jsx
│       └── Auth.jsx
├── config/               # Configuration files
├── uploads/              # User-uploaded PDFs (local only)
├── chromadb_data/        # Persistent ChromaDB vector store
├── pipeline.py           # RAG query pipeline
├── chroma_storage.py     # ChromaDB read/write utilities
├── chromadb_upload.py    # Document ingestion script
├── doc_uploader.py       # PDF parsing and upload handler
├── embedding_utils.py    # Sentence Transformer embeddings
├── text_chunking.py      # PDF text extraction and chunking
├── Modelfile             # Ollama custom model config
├── requirements.txt      # Python dependencies
└── package.json          # Node dependencies
```

---

## Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/) v18+
- [Python](https://python.org/) 3.8+
- [Ollama](https://ollama.com/) - installed and running
- [Git](https://git-scm.com/)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gokulsivas/LexoraAI.git
cd LexoraAI
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd lexora-ui
npm install
```

### 4. Pull the Llama3 Model

```bash
ollama pull llama3
```

---

## Running the Project

Open three terminals and run each of the following:

**Terminal 1 - Ollama**
```bash
ollama serve
# Runs on http://localhost:11434
```

**Terminal 2 - Backend**
```bash
# From the project root
uvicorn app.main:app --reload --port 8000
# API available at http://localhost:8000
```

**Terminal 3 - Frontend**
```bash
cd lexora-ui
npm run dev
# UI available at http://localhost:5173
```

Then open [http://localhost:5173](http://localhost:5173) in your browser.

> **Note:** No environment variables are required. Ensure port `11434` is free for Ollama.

---

## Usage

<div align="center">
  <img src="https://github.com/user-attachments/assets/ef3ba37d-672f-4a66-b2b9-5fadccf74a3b" height="400" style="object-fit: contain;"/>
  <img src="https://github.com/user-attachments/assets/21cbc525-d81e-43bb-95a5-4ba82c470ddb" height="400" style="object-fit: contain;"/>
</div>

1. **Sign up or log in** using the auth form.
2. **Upload a PDF** - e.g., a legal judgment, contract, or notice.
3. **Ask questions** in natural language:
   - *"Summarize the liability section."*
   - *"What are the key obligations of the defendant?"*
   - *"List all dates mentioned in this document."*
4. LexoraAI retrieves the most relevant chunks from your document and streams a response from Llama3 - entirely offline.
5. **Manage files and history** using the UI icons (trash, edit, etc.).

---

## Privacy

All processing happens locally on your machine. Your documents, queries, and responses never leave your device - no API calls to OpenAI, no cloud storage, no telemetry.

---

## Contributing

Contributions are welcome. To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  Built by <a href="https://github.com/gokulsivas">Gokul Sivasubramaniam</a>
</div>
