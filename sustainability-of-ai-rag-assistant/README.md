# Sustainability of AI RAG Research Assistant

A Retrieval-Augmented Generation (RAG) application that answers questions about the environmental impacts of artificial intelligence using a curated corpus of academic research.

The system retrieves relevant sections from research papers, generates grounded answers using an LLM, and cites supporting sources using identifiers such as `[S1]`, `[S2]`, etc.

## Current Features

- Section-aware document chunking
- Content-only retrieval
- Sentence Transformer embeddings (`all-MiniLM-L6-v2`)
- Cosine similarity search
- Grounded LLM-generated responses
- Source attribution and citation tracking
- Provider abstraction (OpenAI, Anthropic, OpenRouter, Ollama)
- Jupyter notebook experimentation workflow
- Working Streamlit web application

## Architecture

```text
Markdown Research Papers
        ↓
load_documents()
        ↓
chunk_by_section()
        ↓
Content Chunks
        ↓
Sentence Transformer Embeddings
        ↓
Cosine Similarity Search
        ↓
retrieve_relevant_chunks()
        ↓
build_context()
        ↓
answer_question()
        ↓
Grounded Response + Sources
```

## Project Structure

```text
data/
├── markdown/                  RAG-ready research papers
└── pdfs/                      Original source PDFs

notebooks/
└── sustainability_of_ai_rag.ipynb
                              Experimentation and evaluation

src/
└── sustainability_rag/
    ├── config.py             Paths, retrieval settings, model configuration
    ├── documents.py          Document loading and chunking
    ├── embeddings.py         Embedding generation
    ├── retrieval.py          Similarity search and context building
    └── rag_pipeline.py       LLM clients, prompt, answer generation

app.py                        Streamlit application
README.md
```

## Current Corpus

Research topics currently include:

- AI energy consumption
- AI carbon emissions
- Training vs. inference impacts
- Data center electricity demand
- Water consumption and cooling
- Hardware lifecycle emissions
- Rebound effects
- Carbon accounting methodologies
- Direct and indirect environmental impacts

Current corpus statistics:

```text
8 research papers
267 total chunks
253 retrieval chunks (content only)
384-dimensional embeddings
```

## Running the Project

### Notebook

Open:

```text
notebooks/sustainability_of_ai_rag.ipynb
```

Restart the kernel and run all cells.

### Streamlit Application

From the project root:

```bash
uv run streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Configuration

API keys are loaded from a `.env` file.

Supported providers:

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
OPENROUTER_API_KEY
```

Model and provider selection are configured in:

```text
src/sustainability_rag/config.py
```

## Current Status

✅ Corpus complete  
✅ Section-aware chunking complete  
✅ Embedding generation complete  
✅ Retrieval pipeline complete  
✅ Grounded answer generation complete  
✅ Source attribution complete  
✅ Notebook refactored into reusable Python package  
✅ Working Streamlit interface  

## Planned Enhancements

- Multipage Streamlit application
- Source explorer page
- Knowledge graph visualization (NetworkX + PyVis)
- Corpus expansion (20-25 research papers)
- Retrieval evaluation framework
- Source diversity filtering
- Hybrid keyword + vector retrieval
- Improved citation tracking
- Public deployment

## Key Learning

The most important lesson from the project so far:

> Retrieval quality depends far more on corpus quality, chunking strategy, and retrieval design than on the choice of LLM.