🧠 Support Knowledge Assistant

A lightweight RAG (Retrieval-Augmented Generation) system built with FastAPI, FAISS, SentenceTransformers, and Ollama.
It acts as a support knowledge assistant that retrieves internal policy documents and generates structured JSON answers following the Model Context Protocol (MCP).

🚀 Features

Semantic retrieval over local Markdown policy files (data/docs/*.md)

Embedding + FAISS vector search (all-MiniLM-L6-v2)

Local LLM generation via Ollama (default: llama3)

Strict JSON responses:

{
  "answer": "...",
  "references": ["..."],
  "action_required": "..."
}

🧩 Project Structure
src/app/
├── main.py              # FastAPI entrypoint
├── retriever.py         # FAISS + embedding retrieval
├── llm_client.py        # Ollama client call
├── prompt_template.py   # System/User prompt templates (MCP)
├── utils.py             # JSON parsing & validation
└── models.py            # Pydantic models

⚙️ Setup & Run
# 1. Create virtual env
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Ollama service
ollama serve
ollama pull llama3

# 4. Run FastAPI app
uvicorn src.app.main:app --reload --port 8000


Access API docs at 👉 http://127.0.0.1:8000/docs

🧪 Example

Request

{
  "ticket_text": "My domain was suspended and I didn’t get any notice. How can I reactivate it?"
}


Response

{
  "answer": "Your domain may have been suspended due to missing WHOIS or unpaid billing. Please correct these and contact support.",
  "references": ["policy domain suspension"],
  "action_required": "request_more_info"
}

✅ Tech Stack

FastAPI – API framework

SentenceTransformers – text embeddings

FAISS – similarity search

Ollama – local LLM inference

Python 3.10+

💡 Notes

Restart the server after editing data/docs to rebuild FAISS index.

Keep Ollama running in the background before starting FastAPI.

Set environment variables if using a custom model:

export OLLAMA_MODEL=llama3
export OLLAMA_HOST=http://localhost:11434