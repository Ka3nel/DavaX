from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parents[1]
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
INDEX_PATH = ROOT_DIR / "src" / "semantic_index.json"
KB_PATH = ROOT_DIR / "data" / "book_summaries.md"
