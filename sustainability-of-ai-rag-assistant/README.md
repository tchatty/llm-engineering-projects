# Sustainability of AI - RAG Research Assistant

A RAG assistant that answers questions about the environmental impacts of AI, using a small curated set of research articles (Markdown versions in `data/markdown/`). Answers cite sources as `[S1]`, `[S2]`, etc.

Notebook-first: experiment in `notebooks/sustainability_of_ai_rag.ipynb`; the reusable code lives in `src/sustainability_rag/` and is also imported by `app.py` (Streamlit placeholder).

## Layout

```
data/markdown, data/pdfs     source articles
notebooks/                   experimentation
src/sustainability_rag/
    config.py                shared constants (paths, TOP_K, models)
    documents.py             load + chunk Markdown
    embeddings.py            embedding model + embeddings
    retrieval.py             similarity search + context building
    rag_pipeline.py          LLM clients, prompt, answer_question
app.py                       Streamlit placeholder
```

## Running

API keys (`OPENAI_API_KEY`, etc.) are read from a `.env` file.

- Notebook: open it and run from the `notebooks/` folder.
- App: from this folder, `streamlit run app.py`
