# LexoraAI

LexoraAI is a privacy-focused, local AI chatbot for querying legal documents using Retrieval-Augmented Generation (RAG). Built with open-source tools, it allows users to upload PDFs, authenticate securely, and get summarized insights from models like Llama3 without cloud dependencies.[1][2]

## Features
- User authentication with JWT-based sign-up and login.
- Intuitive chat interface with auto-scroll and animated backgrounds.
- Document upload and RAG processing: Embed PDFs, retrieve relevant chunks, and generate responses via Ollama.
- Responsive UI with navigation, file management, and real-time streaming replies.[2][5]

## Tech Stack
- Frontend: React, React Router, Lucide React icons, Tailwind CSS.
- Backend: FastAPI, SQLAlchemy (SQLite), Pydantic.
- AI: Ollama (Llama3 model), Sentence Transformers for embeddings, ChromaDB for vector storage.
- Other: Uvicorn server, npm for dependencies.[6][11]

## Prerequisites
- Node.js (for frontend).
- Python 3.8+ (for backend).
- Ollama installed and running (pull Llama3: `ollama pull llama3`).
- Git for cloning.[5][8]

## Installation
1. Clone the repo: `git clone https://github.com/yourusername/lexoraai.git && cd lexoraai`.
2. Backend setup:
   - Create virtual env: `python -m venv venv && venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix).
   - Install deps: `pip install -r requirements.txt`.
3. Frontend setup:
   - `cd frontend && npm install`.
4. Start Ollama: `ollama serve` (runs on localhost:11434).[11][12]

## Running the Project
- Backend: `uvicorn main:app --reload --port 8000` (from root).
- Frontend: `cd frontend && npm start` (runs on localhost:3000).
- Access: Open http://localhost:3000, sign up/login, upload docs, and chat.
- No env vars required, but ensure Ollama port is free.[13][11]

## Usage
- Sign up/login via the auth forms.
- In chat: Upload PDF (e.g., legal judgement), type query like "Summarize section on liability".
- Bot retrieves embeddings, queries Llama3 locally, and streams response.
- Manage files/history via UI icons (trash, edit).[2][6]

## Project Structure
- `/backend`: FastAPI app, models, auth endpoints (main.py, database.py).
- `/frontend/src`: React components (App.jsx, Chat.jsx, Auth.jsx).
- `/uploads`: Stored documents.
- `requirements.txt`: Python deps.
- `package.json`: NPM deps.[1][5]
