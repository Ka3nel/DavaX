# Smart Librarian — Semantic Search Only (Tasks 1–4)

No File Search. No hosted vector store. This project uses a **local semantic index** built from your KB file:
- **Task 1:** `data/book_summaries.md` — your “database” of summaries.
- **Task 2:** Build a vector index locally via OpenAI embeddings (`src/semantic_build_index.py` → writes `src/semantic_index.json`).
- **Task 3:** CLI chatbot that retrieves with semantic search and asks the LLM to pick one title (`src/assistant_cli.py`).
- **Task 4:** `get_summary_by_title(title)` provides a full local summary after the pick (`src/tool_summaries.py`).

## Setup (PyCharm Community, Python 3.13)
```bash
pip install -r requirements.txt
```

## Build the semantic index (one-time or whenever KB changes)
```bash
python -m src.semantic_build_index
```

## Run the chatbot
```bash
python -m src.assistant_cli --k 3
```

Try:
- `I want a book about friendship and magic`
- `What book do you recommend for someone who loves war stories?`

## How it works
- `semantic_build_index.py` parses the KB and embeds each entry with `text-embedding-3-small`.
- `semantic_runtime.search()` embeds the query and ranks by cosine similarity.
- `assistant_cli.py` shows top-k, asks the LLM (`gpt-4o-mini` by default) to pick **exactly one** title (JSON), then prints the **detailed summary** via `get_summary_by_title`.
