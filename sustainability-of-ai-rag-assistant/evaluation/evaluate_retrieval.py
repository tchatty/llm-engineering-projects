import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR / "src"))

from sustainability_rag.documents import (
    build_source_registry,
    chunk_by_section,
    load_documents,
    load_source_metadata,
)
from sustainability_rag.embeddings import embed_chunks
from sustainability_rag.retrieval import retrieve_relevant_chunks

QUESTIONS_PATH = Path(__file__).resolve().parent / "retrieval_questions.json"
REQUIRED_FIELDS = ["id", "question", "expected_source_ids", "expected_sections", "corpus_can_answer"]
EXPECTED_COUNT = 10
TOP_K = 5


def validate_records(records, known_ids, expected_count=EXPECTED_COUNT):
    if len(records) != expected_count:
        sys.exit(f"ERROR: expected {expected_count} records, found {len(records)}.")
    for rec in records:
        missing = [f for f in REQUIRED_FIELDS if f not in rec]
        if missing:
            sys.exit(f"ERROR: {rec.get('id', '?')} is missing fields: {missing}")
        if "REPLACE" in rec["question"]:
            sys.exit(f"ERROR: {rec['id']} still has placeholder question text.")
        if rec["corpus_can_answer"]:
            ids = rec["expected_source_ids"]
            if not ids or any("REPLACE" in i or i not in known_ids for i in ids):
                sys.exit(f"ERROR: {rec['id']} has placeholder or unknown expected source IDs: {ids}")


def evaluate(records, content_chunks, embeddings):
    hits = misses = 0
    coverage = []
    for rec in records:
        if not rec["corpus_can_answer"]:
            coverage.append(rec["id"])
            continue
        results = retrieve_relevant_chunks(rec["question"], content_chunks, embeddings, top_k=TOP_K)
        retrieved = [chunk["source_id"] for chunk, _ in results]
        hit = any(i in retrieved for i in rec["expected_source_ids"])
        hits += hit
        misses += not hit
        print(f"{rec['id']} {'HIT' if hit else 'MISS'}")
        print(f"Question: {rec['question']}")
        print(f"Expected sources: {', '.join(rec['expected_source_ids'])}")
        print(f"Retrieved sources: {', '.join(retrieved)}")
        if not hit:
            if rec["expected_sections"]:
                print(f"Expected sections: {'; '.join(rec['expected_sections'])}")
            print(f"Retrieved sections: {'; '.join(c['section'] for c, _ in results)}")
        print()
    total = hits + misses
    pct = f"{100 * hits / total:.1f}%" if total else "n/a"
    print("SUMMARY")
    print(f"Answerable questions: {total}")
    print(f"Hits: {hits}")
    print(f"Misses: {misses}")
    print(f"Hit@{TOP_K}: {hits}/{total} ({pct})")
    if coverage:
        print("\nCOVERAGE CHECKS")
        for qid in coverage:
            print(f"{qid}: Corpus is labeled as unable to answer this question.")


def main():
    records = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    source_metadata = load_source_metadata()
    source_registry = build_source_registry(source_metadata)
    validate_records(records, set(source_registry.values()))

    chunks = [c for doc in load_documents() for c in chunk_by_section(doc, source_registry)]
    content_chunks = [c for c in chunks if c["type"] == "content"]
    embeddings = embed_chunks(content_chunks)
    evaluate(records, content_chunks, embeddings)


if __name__ == "__main__":
    main()
