"""Build a local semantic index from data/book_summaries.md using OpenAI embeddings.
Writes src/semantic_index.json
Run:
  python -m src.semantic_build_index
"""
import os, re, json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from .config import EMBEDDING_MODEL, KB_PATH, INDEX_PATH

load_dotenv()
client = OpenAI()

def parse_markdown(md: str):
    entries = []
    parts = re.split(r"\n\s*##\s*Title:\s*", md, flags=re.IGNORECASE)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "\n" in part:
            title, summary = part.split("\n", 1)
        else:
            title, summary = part, ""
        text = (title + "\n" + summary.strip()).strip()
        entries.append({"title": title.strip(), "text": text})
    return entries

def main():
    if not KB_PATH.exists():
        raise SystemExit(f"KB file not found: {KB_PATH}")
    md = KB_PATH.read_text(encoding="utf-8")
    docs = parse_markdown(md)
    inputs = [d["text"] for d in docs]
    emb = client.embeddings.create(model=EMBEDDING_MODEL, input=inputs)
    for d, e in zip(docs, emb.data):
        d["embedding"] = e.embedding
    INDEX_PATH.write_text(json.dumps({"model": EMBEDDING_MODEL, "docs": docs}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[build] Wrote {len(docs)} vectors to {INDEX_PATH}")

if __name__ == "__main__":
    main()
