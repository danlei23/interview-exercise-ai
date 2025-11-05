from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .models import TicketIn
from .retriever import retrieve
from .llm_client import call_ollama
from .utils import coerce_json, ensure_mcp

app = FastAPI(title="Support Knowledge Assistant")

@app.post("/resolve-ticket")
def resolve_ticket(body: TicketIn):
    # 1) Perform document retrieval (keep your original k=2)
    hits = retrieve(body.ticket_text, k=2)
    if not hits:
        return JSONResponse({
            "answer": "No relevant policy found. Please escalate.",
            "references": [],
            "action_required": "request_more_info"
        })

    # 2) Build the context and reference list (same as your previous logic)
    refs, ctx_lines = [], []
    for txt, ref in hits:
        ctx_lines.append(f"[{ref}]\n{txt}")
        refs.append(ref)
    context = "\n\n".join(ctx_lines)

    # 3) Call Ollama to generate a response (the model must output strict JSON)
    raw = call_ollama(context=context, ticket=body.ticket_text)

    # 4) Parse and validate the JSON output (prevent the model from returning extra text)
    try:
        data = coerce_json(raw)
        data = ensure_mcp(data)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM output invalid JSON: {e}")

    # 5) If references are empty, fall back to the retrieved document sources
    if not data.get("references"):
        data["references"] = sorted(set(refs))

    return JSONResponse(data)
