import json, math
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from .config import EMBEDDING_MODEL, INDEX_PATH

load_dotenv()
_client = OpenAI()

def _cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = (sum(x*x for x in a)) ** 0.5
    nb = (sum(y*y for y in b)) ** 0.5
    return dot / (na*nb + 1e-12)

def _load_index():
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"semantic_index.json not found at {INDEX_PATH}. Run: python -m src.semantic_build_index")
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))

def search(query: str, k: int = 3):
    idx = _load_index()
    qv = _client.embeddings.create(model=idx.get("model", EMBEDDING_MODEL), input=query).data[0].embedding
    scored = []
    for d in idx["docs"]:
        scored.append((_cosine(qv, d["embedding"]), d["title"], d["text"]))
    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:max(1, k)]
    results = []
    for s, title, text in top:
        snippet = text[:200].replace("\n", " ")
        results.append({"score": float(s), "title": title, "snippet": snippet})
    return results
