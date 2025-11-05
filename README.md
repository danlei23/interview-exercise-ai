# 🧠 Support Knowledge Assistant (RAG)

A lightweight **Retrieval‑Augmented Generation (RAG)** system that helps a support team resolve customer tickets using relevant policy docs. Built with **FastAPI**, **FAISS**, **SentenceTransformers**, and **Ollama**. Responses follow **Model Context Protocol (MCP)** JSON.

---

## 🚀 Overview

The assistant retrieves internal documentation, injects relevant context into prompts, and generates structured JSON answers via a local LLM.

**Example Input**

```
My domain was suspended and I didn’t get any notice. How can I reactivate it?
```

**Example Output (MCP JSON)**

```json
{
  "answer": "Your domain may have been suspended due to missing WHOIS or unpaid billing. Please correct these and contact support.",
  "references": ["policy domain suspension"],
  "action_required": "request_more_info"
}
```

---

## 🧩 Architecture

**Pipeline:** Ticket → FAISS Retriever → Context Injection → LLM (Ollama) → JSON Validation → Response

```
src/app/
├── main.py              # FastAPI entrypoint (POST /resolve-ticket)
├── retriever.py         # FAISS + embedding retrieval
├── llm_client.py        # Ollama client call
├── prompt_template.py   # System/User prompt templates (MCP)
├── utils.py             # JSON parsing & validation
└── models.py            # Pydantic models
```

---

## ⚙️ Setup & Run

### 1️⃣ Environment Setup

Ensure you have:

* Python **3.10+**
* [Ollama](https://ollama.com) installed & running locally

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start Ollama & Pull Model

```bash
ollama serve
ollama pull llama3
```

### 5️⃣ Run FastAPI Server

```bash
uvicorn src.app.main:app --reload --port 8000
```

---

## 🌐 Test via Swagger UI

1. Open your browser at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
2. Scroll to **POST /resolve-ticket**
3. Click **Try it out**
4. Enter a test query, e.g.:

   ```json
   { "ticket_text": "My domain was suspended and I didn’t get any notice. How can I reactivate it?" }
   ```
5. Click **Execute** and view the structured JSON output.

---

## 🧠 Features

✅ Semantic retrieval over `data/docs/*.md`
✅ FAISS + SentenceTransformer embeddings (`all-MiniLM-L6-v2`)
✅ Local inference using Ollama (default model: `llama3`)
✅ MCP‑compliant structured JSON responses

**Response Schema:**

```json
{
  "answer": "...",
  "references": ["..."],
  "action_required": "..."
}
```

---

## ⚙️ Configuration

Optional environment variables:

```bash
export OLLAMA_MODEL=llama3
export OLLAMA_HOST=http://localhost:11434
```

---

## 📚 Data & Indexing

* Place support and policy docs under `data/docs/*.md`
* The FAISS index is automatically built on startup
* **Note:** If you modify documents, restart the app to refresh embeddings

---

## 🧾 Example Request

```json
{
  "ticket_text": "My domain was suspended and I didn’t get any notice. How can I reactivate it?"
}
```

**Example Response**

```json
{
  "answer": "Your domain may have been suspended due to missing WHOIS or unpaid billing. Please correct these and contact support.",
  "references": ["policy domain suspension"],
  "action_required": "request_more_info"
}
```

---

## ✅ Tech Stack

| Component     | Technology           |
| ------------- | -------------------- |
| API           | FastAPI              |
| Embedding     | SentenceTransformers |
| Vector Search | FAISS                |
| LLM           | Ollama (Llama 3)     |
| Language      | Python 3.10+         |

---

## 💡 Notes

* Ensure Ollama is running **before** starting FastAPI
* Restart the server after editing `data/docs`
* Use Swagger UI `/docs` → **POST /resolve-ticket → Try it out** for quick testing
