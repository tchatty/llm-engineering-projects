# Sustainability of AI Research Assistant

## Project Vision and Development Plan

**Document status:** Living project plan  
**Last updated:** October 2026  
**Current stage:** Multipage Streamlit application with a working RAG research assistant  
**Repository:** `llm-engineering-projects/sustainability-of-ai-rag-assistant`

---

## 1. Project Vision

The Sustainability of AI Research Assistant is an evidence-first digital research tool for understanding the environmental and, eventually, broader social risks associated with artificial intelligence.

The project began as a Retrieval-Augmented Generation (RAG) learning exercise using academic papers about AI sustainability. It is evolving into a transparent research application that helps users:

- Find relevant evidence from academic research
- Understand the environmental impacts of AI systems
- Explore uncertainty, disagreement, and limitations in the research
- Compare direct, indirect, operational, and lifecycle impacts
- Make more informed decisions about whether and how AI should be used
- Understand when the application itself uses a generative model
- See what the application does to reduce unnecessary model usage
- Review modeled estimates of the impacts associated with supported LLM calls

The long-term goal is not simply to build another chatbot.

The goal is to build a decision-support and research-exploration tool that demonstrates responsible, restrained, and transparent use of AI.

---

## 2. Mission

Help people understand the environmental and social consequences of widespread AI adoption through accessible evidence, transparent methods, and resource-aware digital tools.

The application should make sustainability research easier to explore without presenting generated text as unquestionable truth.

---

## 3. Core Product Principles

### 3.1 Evidence before generation

The application should retrieve and display relevant research evidence before relying on generated synthesis.

Whenever possible, users should be able to inspect:

- Source ID
- Paper
- Section
- Supporting excerpt
- Retrieval score
- Relevant metadata
- Known limitations

### 3.2 No generative LLM when one is not necessary

The application should provide useful workflows that do not require a live generative-model call.

Planned non-generative response paths include:

- Evidence-only retrieval
- Reviewed research briefs
- Source exploration
- Knowledge-graph exploration
- Cached responses to repeat questions

The application may still use a local embedding model for retrieval. Therefore, this workflow should be called **Evidence Only** or **No-Generation Mode**, not “Non-AI Mode.”

### 3.3 Generate only when synthesis adds value

A live LLM call should be reserved for questions that genuinely benefit from:

- Comparing multiple sources
- Synthesizing findings across papers
- Explaining relationships among concepts
- Summarizing uncertainty or disagreement
- Translating retrieved research into decision-relevant language

### 3.4 Use the smallest adequate model

The default should not be the largest available model.

Model selection should consider:

- Answer quality
- Grounding performance
- Context requirements
- Cost
- Latency
- Resource usage
- Provider support
- Environmental-impact estimation support

### 3.5 Reuse trusted work

The application should reuse reviewed or previously generated content when appropriate.

Preferred response order:

```text
Retrieve relevant evidence
        ↓
Check for an approved research brief
        ↓
Check for a valid exact cached response
        ↓
Use live LLM synthesis only if necessary
```

### 3.6 Make the response pathway visible

Every response should eventually identify how it was produced:

```text
Evidence-only retrieval
Reviewed research brief
Cached generated response
Live generated synthesis
```

Users should not have to guess whether a response was generated in real time.

### 3.7 Preserve provenance

Every substantive response should preserve links to supporting evidence.

Generated synthesis should never replace the underlying sources.

### 3.8 Preserve uncertainty

The application should distinguish among:

- Findings supported by the corpus
- Areas of agreement
- Areas of disagreement
- Methodological differences
- Estimates with significant uncertainty
- Questions unsupported by the current corpus

### 3.9 Be transparent about the application’s own impacts

When the application makes a supported external LLM call, it should eventually disclose:

- Provider and model
- Whether the response was generated live
- Input and output usage when available
- Modeled environmental-impact ranges when defensible
- Estimation method and version
- What the estimate includes
- What the estimate excludes
- Whether environmental estimation was unavailable

Environmental estimates must be presented as modeled approximations, not direct measurements of provider infrastructure.

### 3.10 Add complexity only when evidence supports it

The project should not add vector databases, graph databases, rerankers, hybrid retrieval, or orchestration frameworks merely because they are common AI patterns.

New infrastructure should solve a demonstrated problem.

---

## 4. Intended Users

Potential users include:

- Sustainability professionals
- AI governance teams
- Technology decision-makers
- Researchers and students
- Consultants
- Software and AI engineers
- Organizations evaluating AI use cases
- Members of the public seeking accessible research evidence

The initial version remains a personal research and learning project. It should not be represented as a comprehensive environmental assessment platform.

---

## 5. Current Research Scope

The current corpus focuses primarily on the environmental impacts of AI, including:

- Energy consumption
- Carbon emissions
- Training versus inference impacts
- Data-center electricity demand
- Water consumption and cooling
- Hardware lifecycle impacts
- Embodied emissions
- Carbon-accounting methodologies
- Direct environmental impacts
- Indirect environmental impacts
- Rebound effects
- AI-enabled changes in economic activity

A future phase may expand the project to social risks, but that expansion requires its own scope, inclusion criteria, and evidence base.

Potential future social-risk topics include:

- Labor and supply-chain impacts
- Worker displacement and job redesign
- Data-center impacts on surrounding communities
- Resource-access inequities
- Surveillance and privacy
- Economic and infrastructural concentration
- Accessibility
- Representational harms
- Impacts on affected communities

---

## 6. Current System Architecture

```text
Markdown Research Papers
        ↓
load_documents()
        ↓
Persistent Source Registry
        ↓
chunk_by_section()
        ↓
Content-Only Chunks
        ↓
Sentence Transformer Embeddings
        ↓
Cosine-Similarity Retrieval
        ↓
retrieve_relevant_chunks()
        ↓
build_context()
        ↓
answer_question()
        ↓
Grounded Response + Supporting Sources
```

### Current configuration

```text
Embedding model: all-MiniLM-L6-v2
Embedding dimensions: 384
Top-K retrieval: 5
Default provider: OpenAI
Default model: gpt-4.1-mini
Temperature: 0
Maximum response tokens: 500
```

### Current corpus statistics

```text
Research papers: 8
Total chunks: 267
Retrieval-eligible content chunks: 253
```

These statistics should be updated as the corpus changes.

---

## 7. Current Repository Structure

```text
sustainability-of-ai-rag-assistant/
├── app.py
├── README.md
├── PROJECT_VISION.md
│
├── data/
│   ├── markdown/
│   └── pdfs/
│
├── notebooks/
│   └── sustainability_of_ai_rag.ipynb
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
        ├── config.py
        ├── documents.py
        ├── embeddings.py
        ├── retrieval.py
        └── rag_pipeline.py
```

The notebook remains the experimentation environment.

The reusable application logic lives under `src/sustainability_rag/`.

The Streamlit application provides the user interface.

---

## 8. Current Application Pages

### Research Assistant

**Status:** Working

Provides:

- Natural-language questions
- Semantic retrieval
- Grounded LLM synthesis
- Source citations
- Source details

### Evidence Explorer

**Status:** Placeholder

Planned purpose:

- Retrieve relevant research excerpts
- Avoid generative-model calls
- Show the original supporting evidence
- Explain how semantic retrieval works
- Make weak or uncertain matches visible

### Research Briefs

**Status:** Placeholder

Planned purpose:

- Provide reviewed topic summaries
- Reduce repetitive LLM calls
- Surface agreement and disagreement across papers
- Preserve source and review metadata

### Knowledge Graph

**Status:** Placeholder

Planned purpose:

- Visualize connections among papers and topics
- Reveal research clusters
- Identify corpus gaps
- Support exploration beyond question answering

### Sources

**Status:** Placeholder

Planned purpose:

- Display corpus metadata
- Show persistent source IDs
- Expose paper and section details
- Support corpus quality control

### Impact & Methodology

**Status:** Placeholder

Planned purpose:

- Explain all response pathways
- Disclose when a generative LLM is used
- Explain caching and brief reuse
- Present environmental-impact estimates
- Document estimation boundaries and uncertainty
- Explain limitations of the application

### Application Impact Ledger

The application will maintain a persistent impact ledger for every live LLM inference request initiated through the frontend. Each ledger entry will record the provider, model, response pathway, token usage when available, estimation method and version, and modeled environmental-impact ranges when defensible. The Impact & Methodology page will aggregate compatible entries to show application-lifetime totals and breakdowns by provider, model, and local versus remote inference. The ledger will distinguish measured values, modeled estimates, and calls for which no defensible estimate is available. Evidence-only searches, reviewed research briefs, and cache hits will be counted separately as interactions that avoided an additional live generative-model call. The ledger should minimize retention of user content, preserve methodology versions and system boundaries, and must not present partial inference estimates as the complete lifecycle footprint of the application.

---

## 9. Completed Milestones

### V1: Working RAG pipeline

- [x] Curated initial research corpus
- [x] Converted PDFs into RAG-ready Markdown
- [x] Implemented document loading
- [x] Replaced fixed word-count chunking with section-aware chunking
- [x] Added chunk-type metadata
- [x] Limited retrieval to content chunks
- [x] Added source IDs
- [x] Generated normalized embeddings
- [x] Implemented cosine-similarity retrieval
- [x] Built context from retrieved chunks
- [x] Added grounded answer generation
- [x] Added source attribution
- [x] Added provider abstraction
- [x] Tested representative questions

### V1.1: Reusable application architecture

- [x] Refactored notebook logic into Python modules
- [x] Preserved the notebook experimentation workflow
- [x] Replaced machine-specific data paths
- [x] Added lazy embedding-model loading
- [x] Verified imports outside Jupyter
- [x] Verified notebook behavior after refactoring

### V1.2: Streamlit application shell

- [x] Launched a working Streamlit Research Assistant
- [x] Verified grounded answers through the UI
- [x] Preserved source attribution
- [x] Added multipage navigation
- [x] Added Evidence Explorer placeholder
- [x] Added Research Briefs placeholder
- [x] Added Knowledge Graph placeholder
- [x] Added Sources placeholder
- [x] Added Impact & Methodology placeholder
- [x] Added resource-aware design messaging
- [x] Merged the Streamlit feature branch into `main`

---

## 10. Active Development Plan

The next work should remain incremental.

Only one major feature should be actively implemented at a time.

---

## Phase 1: Evidence-Only Retrieval

**Priority:** Immediate  
**Status:** Next

### Goal

Allow users to search the corpus and inspect relevant evidence without making a generative LLM call.

### Planned user flow

```text
User enters research question
        ↓
Question embedded locally
        ↓
Content chunks ranked by semantic similarity
        ↓
Relevant excerpts displayed
        ↓
No generative LLM call
```

### Planned result fields

- Rank
- Source ID
- Paper or filename
- Section
- Similarity score
- Supporting excerpt

### Required disclosure

The page should clearly communicate:

```text
No generative LLM was used for this search.

The question and research sections were compared using a
sentence-embedding model. Results are ranked by semantic
similarity and should be reviewed by the user.
```

### Design decisions

- [ ] Define the primary user interaction
- [ ] Decide the default number of results
- [ ] Decide excerpt length
- [ ] Decide whether excerpts expand to full sections
- [ ] Explain similarity scores in accessible language
- [ ] Define behavior when all results are weak
- [ ] Define the V1 non-goals

### Implementation

- [ ] Expose a reusable structured evidence-search function
- [ ] Reuse the existing retrieval implementation
- [ ] Replace the Evidence Explorer placeholder
- [ ] Ensure no call to `answer_question()`
- [ ] Ensure no external generative API call
- [ ] Display relevant evidence and provenance

### Validation

Use representative questions:

```text
How much water does AI consume?
What are rebound effects?
How do training and inference impacts differ?
What environmental impacts are associated with model training?
What are indirect environmental impacts?
```

Validate that:

- [ ] Results match the established retrieval workflow
- [ ] Results remain reproducible across application reruns
- [ ] No generated answer is displayed
- [ ] No external LLM request occurs
- [ ] Weak evidence is not presented as a definitive answer
- [ ] The Research Assistant continues to work

---

## Phase 2: Corpus Transparency and Sources

**Priority:** High  
**Status:** Planned

### Goal

Make the contents, coverage, and limitations of the corpus visible.

### Metadata design

Define a canonical metadata schema including:

```text
source_id
filename
title
authors
publication_year
publication_type
doi_or_url
topics
impact_categories
methodologies
geographic_scope
review_status
```

Fields may initially be optional. Missing metadata must remain explicit and must not be silently invented.

### Persistent source registry

Replace ordering-dependent source IDs with a versioned registry.

Requirements:

- [ ] Preserve existing IDs where possible
- [ ] Assign new IDs without renumbering existing sources
- [ ] Detect duplicate IDs
- [ ] Support renamed files
- [ ] Store the registry in a transparent format

### Sources page

Build a functional page showing:

- Corpus statistics
- Paper list
- Source IDs
- Titles and authors
- Publication years
- Topics
- Available sections
- Retrieval eligibility
- Current corpus version

### Corpus versioning

Create a version identifier that changes when:

- Papers are added or removed
- Source IDs change
- Chunking behavior changes
- Retrieval-eligible content changes
- Other retrieval-relevant preprocessing changes

The corpus version will later support:

- Cache invalidation
- Brief provenance
- Evaluation tracking
- Methodology disclosure

---

## Phase 3: Corpus Expansion

**Priority:** High  
**Status:** Planned

### Goal

Expand from 8 papers toward approximately 20–25 papers while maintaining research quality and topic balance.

The target is directional, not a quota.

### Inclusion criteria

Candidate papers should be evaluated for:

- Methodological transparency
- Academic or institutional quality
- Relevance to the project scope
- Direct versus indirect impacts
- Training and inference coverage
- Operational and lifecycle impacts
- Economic and rebound effects
- Geographic diversity
- Areas of agreement and disagreement
- Publication recency
- Duplication with the current corpus

### Process

- [ ] Conduct a corpus gap analysis
- [ ] Identify underrepresented topics
- [ ] Identify candidate papers
- [ ] Review papers manually
- [ ] Select papers using documented criteria
- [ ] Preserve original PDFs
- [ ] Convert papers to RAG-ready Markdown
- [ ] Review headings, references, tables, and metadata
- [ ] Assign persistent source IDs
- [ ] Rebuild chunks and embeddings
- [ ] Update corpus statistics
- [ ] Regression-test known questions

Automatic ingestion should not be prioritized until manual ingestion and quality review are stable.

---

## Phase 4: Reviewed Research Briefs

**Priority:** High  
**Status:** Planned

### Goal

Provide reviewed summaries of frequently requested topics without making a live LLM call.

### Initial topics

- Water consumption
- Training versus inference
- Rebound effects
- Carbon-accounting methodologies

### Brief format

Each brief should contain:

```text
Topic
Short explanation
Key findings
Areas of agreement
Areas of disagreement
Uncertainty and limitations
Decision implications
Supporting source IDs and sections
Corpus version
Review date
Review status
```

### Governance decisions

- [ ] Define what qualifies as reviewed
- [ ] Define who approves a brief
- [ ] Define how disagreements are represented
- [ ] Define how corpus changes affect review status
- [ ] Define whether briefs are written manually or generated once and reviewed
- [ ] Prevent unreviewed generated content from appearing as approved research synthesis

### Implementation

- [ ] Store briefs as transparent Markdown
- [ ] Create a brief index
- [ ] Add provenance metadata
- [ ] Replace the Research Briefs placeholder
- [ ] Display sources and review status
- [ ] Ensure no live LLM call occurs when viewing a brief

---

## Phase 5: Exact-Response Caching

**Priority:** Medium  
**Status:** Planned

### Goal

Avoid repeated calls for identical questions when a valid response already exists.

### Initial scope

Use exact normalized matching only.

Do not implement semantic caching until the risks of returning an answer to a merely similar question are understood.

### Proposed cache key

```text
normalized question
provider
model
prompt version
corpus version
retrieval configuration version
```

### Proposed cached record

```text
question
normalized_question
answer
source_map
retrieved_chunk_ids
provider
model
prompt_version
corpus_version
retrieval_config_version
created_at
impact_estimate
```

### Policy decisions

- [ ] Define normalization behavior
- [ ] Define invalidation behavior
- [ ] Define retention
- [ ] Decide what user content may be stored
- [ ] Define whether cached answers require review
- [ ] Define how cached provenance is displayed
- [ ] Ensure credentials and request headers are never stored

### User disclosure

A cached response should identify:

```text
Response type: Cached generated response
Live LLM calls for this response: 0
Original model:
Original generation date:
Corpus version:
```

### Implementation direction

Use a small local SQLite database unless requirements demonstrate a need for a server-based system.

---

## Phase 6: LLM Environmental-Impact Estimation

**Priority:** Medium  
**Status:** Research required

### Goal

Estimate and disclose the environmental impacts associated with supported live generative-model calls.

### Candidate approach

Evaluate EcoLogits or a comparable open methodology for supported inference requests.

No integration should be added before reviewing:

- Supported providers
- Supported models
- Calculation methodology
- Data sources
- System boundaries
- Estimate ranges
- Model and infrastructure assumptions
- Versioning
- Known limitations

### Initial accounting boundary

The first implementation should cover only:

```text
Supported live external LLM inference initiated by this application
```

It must not imply that the estimate includes:

- Model training
- Local embedding computation
- User-device energy
- Network transmission
- Streamlit hosting
- Storage
- The complete hardware lifecycle
- The complete research workflow

### Display principles

Environmental estimates should:

- Preserve minimum and maximum ranges
- Retain original units
- Identify the estimator and version
- State the provider and model
- Describe the accounting boundary
- Explain known omissions
- Report unsupported estimates as unavailable
- Never report an unavailable estimate as zero

### Proposed disclosure

```text
Estimated impact of this live inference request

These values are modeled estimates, not direct measurements
from the model provider's infrastructure. The estimate covers
the supported inference request and does not represent the
complete lifecycle impact of the application.
```

### Future measurement boundary

Potential future accounting may distinguish:

```text
Remote LLM inference
Local embedding computation
Application hosting
```

Separate estimates should not be combined until boundaries are defined and double counting is addressed.

---

## Phase 7: Impact and Methodology Dashboard

**Priority:** Medium  
**Status:** Planned

### Goal

Make the application’s resource-aware behavior observable.

### Potential session metrics

- Evidence-only searches
- Research briefs viewed
- Cache hits
- Live LLM calls
- Calls with supported impact estimates
- Calls without supported estimates
- Input tokens
- Output tokens

### Response-path disclosure

Each result should identify one of these pathways:

```text
Evidence-only retrieval
Reviewed research brief
Cached generated response
Live generated synthesis
```

### Resource-aware workflow display

Example:

```text
✓ Retrieved local evidence
✓ Checked approved research briefs
✓ Checked exact-response cache
✓ Called an external LLM
✓ Estimated supported inference impacts
```

Or:

```text
✓ Retrieved local evidence
✓ Returned an approved research brief
○ External generative LLM not used
```

### Avoided-call language

The application may report:

```text
3 additional live LLM calls avoided through caching
```

It should not automatically convert avoided calls into “emissions avoided” without a documented counterfactual.

### Methodology page

Document:

- Response pathways
- Retrieval approach
- Model and provider selection
- Cache policy
- Corpus version
- Measurement boundaries
- Estimator and version
- Uncertainty
- Unsupported models
- Known exclusions
- Data-retention policy

---

## Phase 8: Knowledge Graph

**Priority:** Medium  
**Status:** Planned

### Goal

Help users explore relationships within the research corpus.

### User questions the graph should support

- Which topics dominate the corpus?
- Which papers connect water, energy, and carbon impacts?
- Which topics have limited evidence?
- Which research methods recur?
- Which papers connect direct and indirect impacts?
- Where do papers disagree?

### Initial graph schema

Start with only:

```text
Node types:
- Paper
- Topic

Relationship:
- Paper COVERS Topic
```

Do not begin with claim, author, organization, technology, geography, and methodology nodes simultaneously.

### Initial graph data

```text
data/graph/
├── papers.csv
├── topics.csv
└── paper_topics.csv
```

### Controlled vocabulary

Topic names should be reviewed to prevent accidental fragmentation:

```text
Water
Water use
Water consumption
AI water footprint
```

These should only remain separate if the distinction is intentional.

### Implementation direction

Use:

- CSV files for transparent source data
- pandas for loading and validation
- NetworkX for graph construction and analysis
- A Streamlit-compatible visualization method

A graph database such as Neo4j should be considered only if persistence, querying, collaboration, or scale creates a demonstrated need.

### Human review

Graph relationships should not be presented as accepted facts unless reviewed.

If an LLM proposes topics or relationships, store proposals separately until approved.

---

## Phase 9: Retrieval Evaluation

**Priority:** High before retrieval optimization  
**Status:** Planned

### Goal

Determine whether retrieval changes materially improve performance.

The project currently has qualitative evidence that section-aware chunking improved clarity and relevance. It does not yet have a formal benchmark proving retrieval improvement.

### Evaluation set

Create 20–30 reviewed questions covering:

- Energy consumption
- Water
- Carbon emissions
- Training
- Inference
- Hardware lifecycle
- Rebound effects
- Carbon accounting
- Direct impacts
- Indirect impacts
- Method-specific terminology
- Unsupported questions

### Ground truth

For each question, identify:

- Relevant papers
- Relevant sections
- Relevant chunks
- Acceptable alternative evidence
- Whether the corpus can answer the question

### Candidate metrics

- Precision at K
- Recall at K
- Mean Reciprocal Rank
- Source diversity
- Human relevance rating

Only use metrics that can be explained and interpreted.

### Failure categories

- Exact technical term missed
- Correct paper, wrong section
- Multiple relevant sources crowded out
- Mixed-topic chunk
- Insufficient corpus coverage
- Unsupported question
- Weak evidence ranked too highly

### Conditional retrieval improvements

Only implement these if evaluation demonstrates a need:

- Source-diversity filtering
- Hybrid keyword and vector search
- Reranking
- Alternative embedding models
- Smaller section subdivisions
- Metadata filtering
- Persistent vector storage

ChromaDB or another vector database should be introduced for persistence or operational needs, not under the assumption that a vector database automatically improves retrieval quality.

---

## Phase 10: Social-Risk Expansion

**Priority:** Future  
**Status:** Research required

### Goal

Extend the mission beyond environmental impacts without weakening research quality.

### Required decisions

- [ ] Define the social-risk scope
- [ ] Select an organizing framework
- [ ] Define inclusion criteria
- [ ] Decide whether environmental and social evidence belong in one corpus
- [ ] Decide whether impact-domain filtering is required
- [ ] Curate an initial evidence base
- [ ] Update metadata and evaluation methods
- [ ] Review terminology with affected-community perspectives where practical

Possible architecture choices:

```text
One corpus with impact-category metadata
Separate environmental and social corpora
Shared interface with domain filters
```

This expansion should not be treated as a simple topic-tagging exercise.

---

## 11. Potential Future Tools

These ideas remain exploratory and should not be treated as committed scope.

### AI sustainability design advisor

Help users compare design alternatives such as:

- Prompting
- Retrieval
- Fine-tuning
- Small versus large models
- Batch versus real-time inference
- AI versus deterministic software

### “Should I use AI for this?” decision tool

Help users evaluate whether AI adds enough value to justify its costs and risks.

### AI environmental-impact calculator

Estimate workload impacts using transparent inputs, ranges, and uncertainty.

### Responsible AI procurement tool

Help organizations evaluate:

- Provider transparency
- Model choice
- Hosting location
- Resource use
- Environmental reporting
- Governance risks
- Social risks

### Rebound-effect explorer

Illustrate how efficiency improvements may increase total use and produce higher aggregate impacts.

### Paper comparison mode

Compare:

- Methods
- Scope
- Assumptions
- Findings
- Uncertainties
- Areas of disagreement

### Claim-level evidence graph

Connect individual claims to:

- Papers
- Methods
- Supporting evidence
- Contradictory evidence
- Impact categories

---

## 12. Development and Automation Philosophy

Development should follow the same principle as the application:

```text
Think first
Design second
Reuse existing work
Automate repetitive implementation only when valuable
```

### Human-led work

The following work requires human judgment:

- Product vision
- Sustainability framing
- Corpus curation
- Inclusion criteria
- Research briefs
- Environmental accounting boundaries
- Uncertainty language
- Knowledge-graph semantics
- Topic taxonomy
- Evaluation questions
- Relevance labeling
- Social-risk scope
- Transparency and retention policies

### Appropriate limited automation

Claude Code or similar tools may be used conservatively for:

- Streamlit scaffolding
- Repetitive page wiring
- Table rendering
- Small refactors
- SQLite plumbing
- CSV loaders
- NetworkX implementation after graph design
- Test scaffolding
- Documentation formatting

### Automation constraints

When using coding assistants:

- Define scope before starting
- Limit files the assistant may inspect
- Avoid corpus-wide inspection unless necessary
- Avoid unrelated refactoring
- Preserve existing behavior
- Review proposed changes before execution
- Perform manual validation
- Stop after the scoped feature is complete
- Prefer a small number of focused prompts
- Avoid generating architecture merely because it looks sophisticated

---

## 13. Git and Delivery Workflow

Use one feature branch for each coherent capability.

Example:

```text
main
  ↓
feature/evidence-explorer
  ↓
pull request
  ↓
manual validation
  ↓
merge
  ↓
delete branch
```

Potential branches:

```text
feature/evidence-explorer
feature/source-explorer
feature/research-briefs
feature/response-cache
feature/llm-impact-tracking
feature/impact-dashboard
feature/knowledge-graph
feature/retrieval-evaluation
```

### Pull-request expectations

Each pull request should include:

- Purpose
- Scope
- Files or components changed
- Explicit non-goals
- Manual validation performed
- Known limitations
- Screenshots when UI changes are involved
- Confirmation that unrelated functionality remains intact

---

## 14. Project-Management Approach

The project board should remain lightweight.

Recommended columns:

```text
Ideas
Next
In Progress
Validate
Done
```

Recommended limits:

- One primary item in progress
- No more than three items under Next
- Major themes rather than dozens of premature tasks
- Convert work into detailed issues only when it is ready to implement

### Current board

#### In Progress

```text
Design Evidence Explorer
```

#### Next

```text
Implement Evidence Explorer
Validate and document Evidence Explorer
```

#### Ideas

```text
Sources and corpus metadata
Corpus expansion
Reviewed research briefs
Exact-response caching
Environmental-impact estimation
Impact and methodology dashboard
Knowledge graph
Retrieval evaluation
Social-risk expansion
```

#### Done

```text
RAG foundation
Reusable application architecture
Streamlit multipage application shell
```

---

## 15. Success Criteria

The project will be successful when it helps users answer:

```text
What evidence supports this claim?
Which paper and section does the evidence come from?
Was a generative LLM used?
Was the response retrieved, reviewed, cached, or generated?
What uncertainty or disagreement exists?
What does the current corpus not cover?
What environmental-impact estimate is available?
What does that estimate include and exclude?
What did the application do to avoid unnecessary computation?
```

Technical sophistication alone is not success.

Success means the application improves evidence access, decision quality, transparency, and understanding while avoiding unnecessary AI use.

---

## 16. Known Limitations

Current limitations include:

- Small initial corpus
- Predominantly environmental rather than social scope
- No formal retrieval benchmark
- Ordering-dependent source registry pending improvement
- No retrieval-only interface yet
- No research briefs yet
- No response cache yet
- No environmental-impact estimation yet
- No knowledge graph yet
- No public deployment
- Environmental findings are limited to the curated corpus
- Generated responses may simplify or misinterpret research despite grounding controls

These limitations should be updated as the project evolves.

---

## 17. Decision Log

Use this section to preserve important architectural and product decisions.

### Decision: Section-aware chunking

**Reason:** Fixed word-count chunks mixed unrelated ideas and reduced semantic coherence.

### Decision: Content-only retrieval

**Reason:** Abstracts, summaries, and references can introduce duplicated or weakly explanatory matches.

### Decision: NumPy cosine similarity before a vector database

**Reason:** The current corpus is small, and a database does not inherently improve retrieval quality.

### Decision: Streamlit instead of Gradio

**Reason:** The project is evolving into a multipage research and visualization application rather than remaining a chat-only model demo.

### Decision: NetworkX before Neo4j

**Reason:** The graph schema and semantics should be validated before adding graph-database infrastructure.

### Decision: “Evidence Only,” not “Non-AI”

**Reason:** Retrieval still uses a sentence-embedding model even when no generative LLM is called.

### Decision: Exact caching before semantic caching

**Reason:** Similar questions may require materially different answers, and incorrect cache matching could reduce accuracy.

### Decision: Measure before adding hybrid retrieval

**Reason:** Retrieval complexity should address observed benchmark failures rather than assumptions.

### Decision: Impact ranges rather than false precision

**Reason:** Environmental-impact calculations are modeled estimates with uncertain infrastructure and workload assumptions.

---

## 18. Immediate Next Actions

1. Finalize the Evidence Explorer user experience.
2. Define the Evidence Only disclosure.
3. Implement structured retrieval results.
4. Replace the Evidence Explorer placeholder.
5. Verify that no external generative-model call occurs.
6. Validate representative questions.
7. Document retrieval-only behavior and limitations.
8. Merge the completed Evidence Explorer feature into `main`.
9. Begin corpus metadata and persistent source-registry design.

---

## 19. Maintaining This Document

Update this document when:

- Product principles change
- A milestone is completed
- A new major feature is approved
- The corpus scope changes
- The environmental-accounting boundary changes
- Evaluation reveals a major failure mode
- A significant architecture decision is made
- A future idea becomes committed scope

Avoid turning this file into a detailed task tracker.

Use this document for:

- Vision
- Principles
- Architecture
- Milestones
- Major decisions
- Current priorities

Use GitHub Issues and the project board for executable work.