# LLM Engineering Projects

A collection of hands-on projects created while learning and applying large language model engineering, Python application development, prompt design, retrieval systems, and multi-model orchestration.

These projects began as exercises from the **LLM Engineering course by Ed Donner**, but many have been extended beyond the original coursework to explore additional engineering concepts and practical use cases.

This repository serves as:

- A record of my journey learning LLM engineering
- A portfolio of AI applications and experiments
- A playground for exploring new architectures and development patterns
- An incubator for projects that may eventually become standalone repositories

---

## Areas of Exploration

Projects in this repository cover topics including:

- Retrieval-Augmented Generation (RAG)
- Semantic search and embeddings
- Prompt engineering
- Structured LLM inputs and outputs
- Multi-agent systems
- Conversation history and context management
- Gradio interfaces
- Web scraping and document processing
- Streaming model responses
- Local and hosted language models
- Modular Python application design
- AI sustainability research

---

# Projects

## Sustainability of AI RAG Assistant

A Retrieval-Augmented Generation (RAG) research assistant focused on the environmental impacts of artificial intelligence.

The project uses a curated collection of academic papers covering topics such as:

- AI energy consumption
- Model training and inference emissions
- Data center water use
- Hardware lifecycle impacts
- Rebound effects
- Carbon accounting methodologies
- Direct and indirect environmental impacts of AI

The assistant retrieves relevant sections from the research corpus, adds them to the model context, and generates grounded answers with source citations.

### Concepts Explored

- Research paper ingestion
- Markdown document processing
- Section-aware chunking
- Sentence-transformer embeddings
- Cosine similarity retrieval
- Retrieval evaluation
- Context construction
- Grounded answer generation
- Persistent source identifiers
- Source attribution and citations
- Gradio chat interfaces

### Status

✅ V1 complete

### Future Improvements

- Conversation-aware retrieval
- Hybrid keyword + vector search
- Source diversity controls
- Retrieval reranking
- Persistent vector storage
- Evaluation framework
- Paper comparison workflows
- Public deployment

---

## Dynamic Web & PDF Content Summarizer

Extracts and summarizes content from modern websites and embedded PDF documents using an adaptive scraping pipeline.

Supports:

- Static HTML websites
- JavaScript-rendered content
- Linked PDFs
- Embedded PDFs
- Long-document summarization

### Concepts Explored

- Adaptive scraping strategies
- Selenium browser automation
- PDF extraction
- Chunk-based summarization
- Long-context processing
- Separation of extraction and summarization concerns

### Core Technologies

- Requests
- Beautiful Soup
- Selenium
- WebDriver Manager
- PyPDF
- OpenAI

### Future Improvements

- Selenium explicit waits
- Semantic chunking
- Caching
- OCR support
- Additional model providers
- User interface

---

## Prompt Experiment Runner

A lightweight framework for running and managing prompt-engineering experiments using Pydantic and generator-based processing pipelines.

Experiments are defined in JSON, validated with Pydantic, executed against a language model, and stored in structured outputs.

### Concepts Explored

- Pydantic validation
- Type hints
- Structured outputs
- Generator pipelines
- Modular application design
- JSON-driven experimentation

### Example Workflow

```text
experiments.json
        ↓
load_experiments()
        ↓
Pydantic validation
        ↓
Generator pipeline
        ↓
LLM execution
        ↓
ExperimentResult
        ↓
results.json
```

### Future Improvements

- JSONL support
- Batch processing
- Model comparison
- Prompt version tracking
- Experiment scoring
- Async execution

---

## Technical Concept Explainer

An LLM-powered tool for explaining technical concepts and source code using both hosted and local language models.

### Features

- Technical concept explanations
- Source-code explanations
- Few-shot prompting
- Streaming responses
- OpenAI and Ollama support

### Concepts Explored

- Prompt engineering
- Educational AI
- Local models
- Streaming responses
- Few-shot prompting

---

## Three Frontier Models Walk Into a Bar

A multi-agent experiment in which three frontier models debate philosophical topics through a shared conversational memory.

### Models Used

- GPT-4.1 Mini
- Claude
- OpenRouter

### Concepts Explored

- Multi-agent orchestration
- Shared conversational memory
- Agent personas
- Conversation state management
- Emergent LLM behaviors
- Context engineering

### Architecture

```text
Shared Conversation Transcript
                │
                ▼
             GPT
                │
                ▼
            Claude
                │
                ▼
          OpenRouter
                │
                ▼
       Updated Transcript
```

### Future Ideas

- Additional models
- Debate judging
- Belief tracking
- Long-term memory
- Expert-panel simulations
- Tournament-style debates

---

## Open Source Web Scraper

An experimental web scraping project focused on extracting and structuring publicly available web content.

### Concepts Explored

- HTTP requests
- HTML parsing
- Content extraction
- Data cleaning
- Reusable scraping components

This project provided many of the concepts later expanded in the Dynamic Web & PDF Content Summarizer.

---

# Repository Structure

```text
llm-engineering-projects/
├── dynamic-web-pdf-summarizer/
├── opensourcewebscraper/
├── promptexperimentrunner/
├── sustainability-of-ai-rag-assistant/
├── technical_concept_explainer/
├── three-way-LLM-chat/
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

Each project contains its own documentation covering:

- Objectives
- Architecture
- Dependencies
- Setup
- Design decisions
- Limitations
- Future enhancements

---

# Development Environment

This repository uses Python and `uv` for dependency and environment management.

## Create Environment

```powershell
uv venv
```

## Synchronize Dependencies

```powershell
uv sync
```

## Activate Environment

```powershell
.venv\Scripts\Activate.ps1
```

## Install Jupyter Kernel

```powershell
python -m ipykernel install --user --name llm-engineering-projects --display-name "LLM Engineering Projects"
```

Select the **LLM Engineering Projects** kernel when opening notebooks.

---

# Environment Variables

Some projects require access to hosted model APIs.

Create a local `.env` file:

```env
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
OPENROUTER_API_KEY=
```

The `.env` file is excluded from Git and should never be committed.

An `.env.example` file can be committed to document required variables without exposing credentials.

---

# Running a Project

Most projects follow a simple workflow:

1. Clone the repository
2. Create or synchronize the environment
3. Add API credentials to `.env`
4. Select the project kernel
5. Open the relevant notebook or Python entry point
6. Follow the instructions in the project README

Individual projects may have additional requirements.

---

# Repository Philosophy

The goal of this repository is to learn AI engineering by building practical systems rather than isolated examples.

Projects intentionally begin with simple implementations so the underlying concepts remain visible:

- Chunking
- Embeddings
- Retrieval
- Prompt construction
- Context management
- Agent orchestration

As projects mature, they may be refactored into more production-oriented architectures or moved into dedicated repositories.

---

# Learning Roadmap

Areas of continued exploration include:

- Advanced RAG architectures
- Hybrid retrieval and reranking
- Agent workflows
- Evaluation and observability
- Structured model outputs
- MCP (Model Context Protocol)
- Human-in-the-loop systems
- Vector databases
- Cloud deployment
- Sustainability analytics
- Climate decision-support tools
- Enterprise AI workflows

---

# Responsible Use

These projects are intended for learning, experimentation, and portfolio development.

Please do not commit:

- API keys
- Credentials
- Proprietary code
- Client information
- Internal documentation
- Sensitive datasets

Model-generated outputs should be reviewed before being used for research, professional decisions, sustainability analysis, or other consequential purposes.

---

# Author

**Teja Chatty**

Building practical skills across:

- LLM Engineering
- Python Development
- AI Application Architecture
- Data Science
- Sustainability Analytics
- Climate Technology

---

# Acknowledgements

Several projects in this repository began as exercises inspired by the **LLM Engineering course by Ed Donner** and were later extended through independent experimentation and development.
``