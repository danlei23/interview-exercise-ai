import os
import ollama
from .prompt_template import SYSTEM_PROMPT, USER_TEMPLATE

def call_ollama(context: str, ticket: str) -> str:
    model = os.getenv("OLLAMA_MODEL", "llama3")
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    # ✅ Create a Client instance and specify the host (more stable than using ollama.chat() directly)
    client = ollama.Client(host=host)

    resp = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(context=context, ticket=ticket)},
        ],
        options={"temperature": 0.2},
    )

    return resp["message"]["content"].strip()