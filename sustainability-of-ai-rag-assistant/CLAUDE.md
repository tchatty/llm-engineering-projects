# CLAUDE.md — Sustainability of AI Research Assistant

Evidence-first Streamlit RAG app on a small curated corpus. The owner is a sustainability expert and an advanced beginner in ML/RAG. This project is about restrained AI use, and development should be too.

## Operating rules (always apply)

1. **Minimal tokens.** Read only the files the task needs. Don't explore the repo "for context." Use Grep or line ranges, not whole-file reads. Don't spawn subagents or workflows unless asked.
2. **Strict scope.** Build only what was asked. No extra features, refactors, abstractions, config options, or "while I'm here" fixes. If you spot something worth doing, mention it in one line; don't do it.
3. **Plan before coding when it's ambiguous.** If the task touches more than about 3 files or needs a design choice, give a short plan (5 bullets max) and wait. For small, clear tasks, just do them.
4. **Short output.** No preamble, no recaps of what you just did beyond 1–3 lines, no repeating code back. Explain concepts briefly when the owner asks, or when a change brings in an ML/RAG idea they may not know (one or two sentences).
5. **Don't add infrastructure** (vector DBs, graph DBs, rerankers, LangChain/orchestration, new services) without a demonstrated problem. See plan §3.10 and §17.
6. **Prefer stdlib and existing deps.** Ask before adding a dependency.
7. **Stop when the scoped task is done.** Don't chain into the next phase.

## Expensive files: don't read unless the task requires it

- `project_plan.md` (~1,500 lines): read only the section you need (e.g. grep for `## Phase 4`).
- `data/markdown/*`: large corpus papers. Never bulk-read them. Grep for specific terms.
- `data/pdfs/*`, `notebooks/*.ipynb`, `.venv/`, `../.env`: never read them.

## Layout

- `app.py` + `pages/*.py`: Streamlit UI (multipage).
- `src/sustainability_rag/`: `config.py` (paths, models), `documents.py` (load + section chunking), `embeddings.py` (all-MiniLM-L6-v2, lazy load), `retrieval.py` (NumPy cosine, top-k, `build_context`), `rag_pipeline.py` (provider clients, `answer_question`).
- Notebook = experimentation. Reusable logic goes in `src/`, not in pages.
- Deps are managed with `uv` from the monorepo root (`../pyproject.toml`).

## Commands

- Run app: `uv run streamlit run app.py` (from this directory). Don't launch it unless asked; the owner validates the UI by hand.
- Quick import check: `uv run python -c "import sustainability_rag"`.

## Domain invariants (don't violate)

- **Evidence-only paths must never call `answer_question()` or any generative API.** Call it "Evidence Only", never "Non-AI".
- Preserve provenance: source ID, paper, section, and excerpt must stay attached to results.
- Never invent metadata. Missing fields stay explicit (`None` or "unknown").
- Impact estimates are **ranges** with estimator and version. "Unavailable" is never shown as zero. Avoided calls are not converted to "emissions avoided."
- Don't write sustainability framing, research briefs, topic taxonomy, eval labels, or uncertainty language on your own. These are owner-led. Draft only if asked, and label drafts as unreviewed.
- Never log or store API keys or request headers. Keep stored user content to a minimum.

## Code style

Match the surrounding code. Small functions, type hints where existing code uses them, few comments. Don't reformat untouched code.

## Git

One feature branch per capability (`feature/<name>`). Commit or push only when asked. PR body: Purpose, Scope, Files, Non-goals, Validation, Limitations.
