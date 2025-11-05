import os, glob
import faiss, numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

_EMB_MODEL = None
_INDEX = None
_CHUNKS = None

def _load_docs_to_chunks():
    """
    Read all Markdown files from data/docs/*.md and treat each file as a single chunk (sufficient for the MVP).
    For higher accuracy in the future, you can modify this to split documents by paragraph or section level.
    """
    chunks = []
    for path in glob.glob(os.path.join("data", "docs", "*.md")):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        ref = os.path.basename(path).replace("_", " ").replace(".md", "")
        chunks.append({"text": text, "ref": ref})
    return chunks

def _ensure_index():
    global _EMB_MODEL, _INDEX, _CHUNKS
    if _INDEX is not None:
        return
    _CHUNKS = _load_docs_to_chunks()
    texts = [c["text"] for c in _CHUNKS]
    _EMB_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vecs = _EMB_MODEL.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    dim = vecs.shape[1]
    _INDEX = faiss.IndexFlatIP(dim)
    _INDEX.add(vecs)

def retrieve(query: str, k: int = 4) -> List[Tuple[str, str]]:
    _ensure_index()
    q = _EMB_MODEL.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    sims, idxs = _INDEX.search(q, k)
    results = []
    for i in idxs[0]:
        c = _CHUNKS[i]
        results.append((c["text"], c["ref"]))
    return results
