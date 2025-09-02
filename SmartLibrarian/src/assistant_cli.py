"""Semantic-search–only CLI.
Flow:
  1) Retrieve top-k titles via local embeddings + cosine.
  2) Ask the LLM to pick EXACTLY ONE and return JSON.
  3) Print a detailed summary via get_summary_by_title().
Run:
  python -m src.assistant_cli --k 3
"""
import json, os, sys
import typer
from dotenv import load_dotenv
from openai import OpenAI
from .config import CHAT_MODEL
from .semantic_runtime import search as sem_search
from .tool_summaries import get_summary_by_title

load_dotenv()
client = OpenAI()
app = typer.Typer(add_completion=False)

def llm_pick(candidates, user_query: str) -> dict:
    system = (
        "You are a helpful book-recommendation assistant. "
        "Given the user's interests and the candidate titles, respond ONLY with JSON: "
        "{\"title\": \"<exact title from candidates>\", \"rationale\": \"<1-2 sentences>\"}"
    )
    msg = (
        f"User query: {user_query}\n"
        f"Candidate titles (ranked): {candidates}\n"
        "Return strictly the JSON with 'title' and 'rationale'."
    )
    resp = client.chat.completions.create(
        model=CHAT_MODEL, temperature=0,
        messages=[{"role":"system","content":system},{"role":"user","content":msg}]
    )
    text = resp.choices[0].message.content or ""
    try:
        return json.loads(text)
    except Exception:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try: return json.loads(text[start:end+1])
            except Exception: return {"title": candidates[0], "rationale": "Top-ranked match."}
        return {"title": candidates[0], "rationale": "Top-ranked match."}

@app.command()
def main(k: int = typer.Option(3, help="top-k candidates")):
    print("Smart Librarian — Semantic Search only (Ctrl+C to exit)")
    while True:
        try:
            user_query = input("\nYou: ").strip()
            if not user_query:
                continue
            top = sem_search(user_query, k=k)
            if not top:
                print("No semantic matches found. Try another query.")
                continue
            print("[semantic] Top candidates:")
            candidates = [t["title"] for t in top]
            for i, t in enumerate(top, 1):
                print(f"  {i}. {t['title']} (score={t['score']:.4f}) — {t['snippet']}")
            choice = llm_pick(candidates, user_query)
            title = choice.get("title", candidates[0])
            print("\nAssistant (JSON):", json.dumps(choice, ensure_ascii=False))
            print(f"\nDetailed summary for '{title}':\n{get_summary_by_title(title)}")
        except (KeyboardInterrupt, EOFError):
            print("\nBye!"); break

if __name__ == "__main__":
    app()
