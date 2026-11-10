# CodeCarbon Experiment Protocol

## 1\. Purpose

Evaluate whether CodeCarbon is suitable for assessing local computation performed by the Sustainability of AI application.

The experiment will determine whether CodeCarbon produces sufficiently granular, repeatable, and interpretable results to support:

- Internal application\-design decisions
- User\-facing environmental disclosures
- Application\-lifetime impact aggregation

The application boundary, response pathways, operation definitions, classifications, and exclusions are defined in docs/impact\_accounting\_scope.md. That document is the source of truth for methodology context and must not be duplicated here.

## 2\. Research Questions

### RQ1: Compatibility

Does CodeCarbon work on the target Windows hardware, and can its measurement basis be identified for CPU, GPU, and RAM?

### RQ2: Reliability and granularity

Can CodeCarbon produce repeatable and interpretable results for:

- Cold\-start corpus\-resource construction
- Batched semantic\-retrieval operations

Are retrieval operations measurable directly, or is a batch\-derived allocation required?

### RQ3: Suitability

Are the results and their provenance sufficient for:

- Comparing application\-design alternatives
- Communicating impacts without false precision
- Retaining compatible results for application\-lifetime aggregation

## 3\. Experiment Design

### Experiment 1: Environment compatibility

Run CodeCarbon hardware detection and a deterministic smoke test.

Record:

- CodeCarbon version
- Python version
- Operating system
- CPU model
- GPU model
- Installed RAM
- Tracking mode
- Sampling interval
- Geographic assumption
- Electricity carbon\-intensity assumption
- Hardware warnings
- Missing components
- Available telemetry
- Evidence of fallback power modeling

The smoke\-test workload should run for at least 60 seconds and be repeated three times.

#### Purpose

Confirm that CodeCarbon:

- Runs successfully on the target hardware
- Produces native output
- Identifies the relevant hardware
- Returns nonmissing duration, energy, and emissions fields
- Provides enough information to describe whether results are measured, modeled, or partially measured

### Experiment 2: Cold\-start corpus resources

Measure the uncached construction of the shared corpus resources.

The measured operation should include:

1. Loading reviewed source metadata
2. Loading Markdown documents
3. Validating source metadata
4. Creating stable source mappings
5. Creating section\-based chunks
6. Retaining retrieval\-eligible content chunks
7. Loading the embedding model
8. Generating normalized corpus embeddings

Run each repetition in a new Python process.

Complete three valid repetitions.

For each repetition, validate:

- Expected source\-document count
- Expected content\-chunk count
- Expected embedding dimensions
- Successful metadata validation
- Successful embedding completion

Record:

- Duration
- Total energy
- CPU energy
- GPU energy
- RAM energy
- Greenhouse\-gas emissions
- Warnings
- Missing values

#### Purpose

Determine whether CodeCarbon can characterize the local impact of constructing corpus resources after a complete application restart.

### Experiment 3: Retrieval batch

Initialize corpus resources before measurement.

Run ten unmeasured warm\-up searches, then measure:

- 100 retrieval operations
- Three repetitions

Cycle through the existing reviewed retrieval questions.

If the measured workload is too short relative to the CodeCarbon sampling interval, repeat with:

- 1,000 retrieval operations
- Three repetitions

Each retrieval must use the existing production retrieval implementation. The experiment must not create a second similarity\-ranking implementation.

Record:

- Requested operation count
- Completed operation count
- Failed operation count
- Top\-K
- Chunk count
- Embedding model
- Total duration
- Total energy
- CPU energy
- GPU energy
- RAM energy
- Greenhouse\-gas emissions
- Warnings
- Missing values

Do not store question text, retrieved passages, citations, or source\-document content in experiment results.

#### Purpose

Determine whether batched retrieval produces sufficiently stable results for a possible derived per\-search allocation.

Claude Code must not calculate a per\-search allocation during the initial experiment. That calculation requires human approval after review of the batch results.

### Experiment 4: Shared\-resource verification

Verify manually that:

1. Start Here does not initialize corpus resources.
2. Evidence Explorer initializes corpus resources once.
3. Research Assistant reuses the initialized resources.
4. Corpus embeddings are not recomputed during the page transition.

Use deterministic application behavior, existing cache semantics, or temporary noncommitted logging for verification.

CodeCarbon results may supplement this verification, but CodeCarbon results alone are not proof that initialization occurred exactly once.

Claude Code must not modify Streamlit pages or production modules to implement this verification during the initial experiment.

## 4\. Repetition and Summary Requirements

For each measured workload, report:

- Number of valid repetitions
- Number of failed repetitions
- Minimum
- Maximum
- Median
- Arithmetic mean
- Standard deviation
- Coefficient of variation

Calculate these statistics for:

- Duration
- Total energy
- CPU energy
- GPU energy
- RAM energy
- Greenhouse\-gas emissions

Claude Code may calculate descriptive statistics. Claude Code must not determine whether the results are sufficiently reliable or suitable for disclosure.

## 5\. Output Requirements

Preserve CodeCarbon native output.

Also create a sanitized experiment manifest containing:

- Experiment identifier
- Experiment type
- Timestamp
- Git commit
- CodeCarbon version
- Python version
- Operating system
- Tracking configuration
- Corpus version or corpus fingerprint
- Embedding model
- Chunk count
- Retrieval Top\-K
- Requested operation count
- Completed operation count
- Failed operation count
- CodeCarbon run identifier
- Native output filename
- Execution status
- Warnings

Missing values must remain missing. Missing values must never be converted to zero.

Raw output containing hardware, geographic, or operating\-system metadata must remain local and excluded from source control.

## 6\. Repository Access

### Permitted files to inspect

Claude Code may inspect only:

- docs/codecarbon\_experiment\_protocol.md
- docs/impact\_accounting\_scope.md
- docs/impact\_decision\_log.md
- CLAUDE.md
- src/sustainability\_rag/\_\_init\_\_.py
- src/sustainability\_rag/config.py
- src/sustainability\_rag/resources.py
- src/sustainability\_rag/documents.py
- src/sustainability\_rag/embeddings.py
- src/sustainability\_rag/retrieval.py
- evaluation/evaluate\_retrieval.py
- evaluation/retrieval\_questions.json
- ../pyproject.toml
- ../uv.lock
- ../.gitignore

Claude Code may inspect one additional module only if a permitted file directly imports it and the additional module is required to execute the experiment.

Every additional file inspected must be reported.

### Files and directories not to inspect

Claude Code must not inspect:

- data/markdown/
- data/pdfs/
- notebooks/
- project\_plan.md
- pages/
- src/sustainability\_rag/rag\_pipeline.py
- Environment\-variable values
- API keys
- Unrelated projects in the parent repository

The restriction against inspecting corpus contents applies to Claude Code repository analysis. It does not prevent the approved experiment script from loading the corpus at runtime through the existing load\_documents() function.

Claude Code must not substitute synthetic documents for the real corpus.

## 7\. Permitted Deliverables

Claude Code may create:

- evaluation/measure\_local\_compute.py
- evaluation/summarize\_codecarbon\_results.py
- evaluation/impact\_results/README.md
- Focused tests for command\-line configuration, manifest creation, result sanitization, and summary calculations

Generated local results should use:

- evaluation/impact\_results/codecarbon/

Only the directory README should be committed. Raw CSV, JSON, log, and hardware\-detection outputs must remain excluded from source control.

## 8\. Implementation Constraints

Claude Code must:

- Reuse the existing document\-loading, embedding, resource\-construction, and retrieval functions
- Preserve CodeCarbon native output
- Disable CodeCarbon cloud upload
- Use command\-line arguments for experiment configuration
- Keep generated machine\-specific results outside source control
- Treat missing results as missing or failed, never zero
- Initialize corpus resources before starting retrieval\-batch tracking
- Perform retrieval warm\-up before starting measurement
- Use reviewed retrieval questions cyclically
- Record successfully completed operation counts
- Keep helper functions small and experiment\-specific

Claude Code must not:

- Modify production application behavior
- Modify retrieval methodology
- Change the embedding model
- Change production Top\-K
- Add persistent frontend instrumentation
- Add a database
- Add a dashboard
- Upload results to an external service
- Subtract idle results
- Create a custom environmental methodology
- Calculate per\-search allocations before human approval
- Interpret whether results are reliable
- Commit raw machine\-specific results

## 9\. Automated Validation

Claude Code may run:

- Python syntax checks
- Experiment script help commands
- Result\-summary script help commands
- Focused unit tests
- Short synthetic validation runs that do not represent environmental measurements

Claude Code must not run:

- Three 60\-second smoke tests
- Cold\-start measurement repetitions
- Full retrieval batches
- Long\-running experiments
- Streamlit instrumentation
- Experiments requiring controlled background conditions

The human reviewer will run all controlled measurements.

## 10\. Required Claude Code Report

Claude Code must return:

- Current branch
- Files inspected
- Additional files inspected, if any
- Files created or changed
- Dependency changes
- Commands executed
- Automated validation results
- Manual experiment commands
- Expected result\-file locations
- Known implementation limitations
- Assumptions introduced by the implementation

The report must not interpret environmental results or recommend integration.

## 11\. Human Decision Gate

After reviewing the results, the human reviewer will select one outcome.

### Integrate

Use CodeCarbon in the application because the measurement basis and results are sufficiently interpretable.

### Controlled experiments only

Use CodeCarbon for benchmark studies but not per\-interaction disclosure.

### Batch\-derived allocation

Use stable retrieval batches to derive a clearly labeled per\-search allocation.

### Supplement

Combine CodeCarbon with additional hardware telemetry or external power measurement.

### Replace or customize

Develop an application\-specific calculation method only if CodeCarbon cannot represent the target hardware or operations and a defensible alternative can be validated.