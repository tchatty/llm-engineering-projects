# Sustainability of AI Research Assistant

An evidence-first research application for exploring the environmental impacts of artificial intelligence through a curated corpus of academic papers.

The project uses Retrieval-Augmented Generation (RAG) to locate relevant research sections, generate grounded answers when synthesis is useful, and cite supporting sources using identifiers such as `[S1]` and `[S2]`.

The long-term goal is not simply to build a chatbot. It is to create a transparent research and decision-support tool that helps users inspect evidence, understand uncertainty, and learn about AI’s environmental and social risks while minimizing unnecessary generative-model use.

## Product Principles

The application is being developed around the following principles:

1. **Retrieve evidence before generating text**
2. **Provide useful workflows that do not require a generative LLM**
3. **Reuse reviewed research briefs before making live model calls**
4. **Reuse valid cached responses for repeated questions**
5. **Use the smallest adequately performing model when generation is necessary**
6. **Disclose whether a response was retrieved, reviewed, cached, or generated**
7. **Preserve source provenance and research uncertainty**
8. **Estimate and disclose the impacts of supported live LLM calls**
9. **Add technical complexity only when evaluation demonstrates a need**

## Current Features

- Curated corpus of academic research
- Section-aware document chunking
- Content-only retrieval
- Sentence Transformer embeddings using `all-MiniLM-L6-v2`
- Normalized cosine-similarity search
- Grounded LLM-generated responses
- Source attribution and citation tracking
- Provider abstraction for OpenAI, Anthropic, OpenRouter, and Ollama
- Notebook-based experimentation workflow
- Reusable Python package
- Working multipage Streamlit application

## Application Pages

### Research Assistant

The working RAG question-answer interface.

The page:

- Accepts natural-language questions
- Retrieves relevant research sections
- Generates a grounded synthesis
- Cites supporting sources
- Displays the sources used

### Evidence Explorer

Planned retrieval-only interface for displaying relevant research excerpts without making a generative LLM call.

Expected results will include:

- Source ID
- Paper
- Section
- Similarity score
- Supporting excerpt

This mode will still use a sentence-embedding model for retrieval, so it is described as **Evidence Only**, not “Non-AI.”

### Research Briefs

Planned collection of reviewed, precomputed summaries for frequently explored topics.

Potential initial briefs include:

- Water consumption
- Training versus inference
- Rebound effects
- Carbon-accounting methodologies

Research briefs will provide useful synthesis without making a new live LLM call each time they are viewed.

### Knowledge Graph

Planned visualization of relationships among research papers and sustainability topics.

The initial graph will likely use:

- Paper nodes
- Topic nodes
- `COVERS` relationships

The graph schema and topic vocabulary will be designed before selecting permanent graph infrastructure.

### Sources

Planned corpus-exploration interface showing:

- Persistent source IDs
- Paper metadata
- Authors and publication years
- Research topics
- Sections
- Corpus statistics
- Retrieval eligibility

### Impact & Methodology

Planned transparency center explaining:

- How responses are produced
- When a generative LLM is used
- Evidence-only workflows
- Research-brief reuse
- Response caching
- Model and provider selection
- Environmental-impact estimation
- System boundaries and uncertainty
- Known application limitations

This page will eventually include an application impact ledger that tallies compatible environmental-impact estimates across live LLM calls made through the frontend.

## Intended Response Pathways

The application is evolving toward four clearly disclosed response pathways:

```text
Evidence-only retrieval
Reviewed research brief
Cached generated response
Live generated synthesis
```

The intended decision flow is:

```text
User submits a question
        ↓
Retrieve relevant evidence
        ↓
Check for an approved research brief
        ↓
Check for a valid exact cached response
        ↓
Use live LLM synthesis only if necessary
        ↓
Record response provenance and supported impact estimates
```

## Architecture

```text
Markdown Research Papers
        ↓
load_documents()
        ↓
chunk_by_section()
        ↓
Content-Only Chunks
        ↓
Sentence Transformer Embeddings
        ↓
Cosine-Similarity Search
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
sustainability-of-ai-rag-assistant/
├── app.py
├── README.md
├── PROJECT_VISION.md
│
├── data/
│   ├── markdown/                  RAG-ready research papers
│   └── pdfs/                      Original source PDFs
│
├── notebooks/
│   └── sustainability_of_ai_rag.ipynb
│                                      Experimentation and evaluation
│
├── pages/
│   ├── research_assistant.py
│   ├── evidence_explorer.py
│   ├── research_briefs.py
│   ├── knowledge_graph.py
│   ├── sources.py
│   └── impact_methodology.py
│
└── src/
    └── sustainability_rag/
        ├── __init__.py
        ├── config.py               Paths and model configuration
        ├── documents.py            Document loading and chunking
        ├── embeddings.py           Embedding generation
        ├── retrieval.py            Similarity search and context building
        └── rag_pipeline.py         LLM clients and answer generation
```

The notebook remains the experimentation environment.

The reusable application logic lives under `src/sustainability_rag/`.

The Streamlit pages provide the user interface.

## Current Corpus

The current corpus contains eight research papers covering topics such as:

- AI energy consumption
- AI carbon emissions
- Training versus inference impacts
- Data-center electricity demand
- Water consumption and cooling
- Hardware lifecycle emissions
- Rebound effects
- Carbon-accounting methodologies
- Direct and indirect environmental impacts

Current corpus statistics:

```text
Research papers: 8
Total chunks: 267
Retrieval-eligible content chunks: 253
Embedding dimensions: 384
```

The corpus is expected to expand toward approximately 20–25 carefully selected papers. This is a directional target rather than a quality-independent quota.

## Configuration

Current defaults:

```text
Embedding model: all-MiniLM-L6-v2
Top-K retrieval: 5
Default provider: OpenAI
Default model: gpt-4.1-mini
Temperature: 0
Maximum response tokens: 500
```

Provider and model selection are configured in:

```text
src/sustainability_rag/config.py
```

API credentials are loaded from a local `.env` file.

Potential variables include:

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
OPENROUTER_API_KEY
```

The `.env` file must not be committed to version control.

## Running the Project

### Install dependencies

From the repository root:

```bash
uv sync
```

### Run the notebook

Open:

```text
notebooks/sustainability_of_ai_rag.ipynb
```

Restart the kernel and run all cells.

The notebook is used for:

- Corpus inspection
- Chunking experiments
- Retrieval evaluation
- Prompt experimentation
- Answer inspection

### Run the Streamlit application

From the `sustainability-of-ai-rag-assistant` directory:

```bash
uv run streamlit run app.py
```

Then open the local URL displayed by Streamlit, typically:

```text
http://localhost:8501
```

## Current Status

### Completed

- [x] Initial research corpus
- [x] PDF-to-Markdown conversion
- [x] Section-aware chunking
- [x] Content-only retrieval
- [x] Embedding generation
- [x] Cosine-similarity retrieval
- [x] Grounded answer generation
- [x] Source attribution
- [x] Provider abstraction
- [x] Reusable Python package
- [x] Notebook experimentation workflow
- [x] Working Streamlit Research Assistant
- [x] Multipage Streamlit application shell
- [x] Feature placeholders for the planned research workflows

### Next

- [ ] Design the Evidence Explorer user experience
- [ ] Implement retrieval-only evidence search
- [ ] Validate and document Evidence Explorer limitations

### Planned

- [ ] Persistent source registry
- [ ] Functional Sources page
- [ ] Corpus metadata schema
- [ ] Corpus expansion
- [ ] Reviewed research briefs
- [ ] Exact-response caching
- [ ] Per-response LLM impact estimates
- [ ] Application-lifetime impact ledger
- [ ] Impact & Methodology dashboard
- [ ] Knowledge-graph prototype
- [ ] Retrieval evaluation framework
- [ ] Social-risk research expansion

## Environmental-Impact Transparency

The application is intended to disclose environmental-impact information for supported live LLM calls.

Planned per-response disclosure includes:

- Provider and model
- Local or remote execution
- Token usage when available
- Modeled environmental-impact ranges
- Estimation method and version
- Accounting boundary
- Known exclusions
- Whether an estimate is unavailable

The application will also maintain an impact ledger for live LLM calls made through the frontend. Compatible request-level records will be aggregated on the Impact & Methodology page to provide application-lifetime totals and breakdowns.

The ledger will distinguish among:

- Modeled estimates
- Measured local-compute values
- Calls without defensible estimates
- Evidence-only searches
- Research-brief views
- Cache hits
- Local-model calls
- Remote-model calls

These values will not be presented as the complete lifecycle footprint of the application.

## Evaluation Strategy

Retrieval changes will be evaluated before adding architectural complexity.

Planned evaluation includes:

- Reviewed benchmark questions
- Relevant-source and relevant-chunk labels
- Precision at K
- Recall at K
- Ranking quality
- Source diversity
- Human relevance review
- Retrieval-failure categorization

Potential improvements such as hybrid search, source-diversity filtering, reranking, or alternative embedding models will only be prioritized when evaluation reveals a material retrieval problem.

## Known Limitations

- The current corpus is small
- The present scope is primarily environmental
- Retrieval performance has not yet been measured against a formal benchmark
- Source IDs are not yet stored in a persistent registry
- Evidence Explorer is not yet implemented
- Research briefs are not yet implemented
- Cached response reuse is not yet implemented
- Environmental-impact accounting is not yet implemented
- Knowledge-graph exploration is not yet implemented
- Generated responses can still simplify or misinterpret research
- Answers are limited to the evidence contained in the curated corpus

## Project Scope

This is currently a research, learning, and portfolio project.

The application should not be treated as:

- A comprehensive environmental assessment
- A substitute for reading the source research
- A definitive model-comparison tool
- A verified lifecycle assessment of AI systems
- Professional environmental, legal, or regulatory advice
