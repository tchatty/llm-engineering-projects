# EcoLogits Experiment Protocol

## 1\. Purpose

Evaluate whether EcoLogits is suitable for estimating the environmental impacts of supported remote generative\-model calls made by the Sustainability of AI Research Assistant.

The experiment will determine whether EcoLogits produces sufficiently complete, interpretable, and reproducible results to support:

- Internal application\-design decisions
- User\-facing per\-response disclosures
- Application\-lifetime impact aggregation

The application boundary, response pathways, operation definitions, classifications, and exclusions are defined in docs/impact\_accounting\_scope.md. That document is the source of truth for methodology context and must not be duplicated here.

## 2\. Research Questions

### RQ1: Compatibility

Does EcoLogits work with the application's provider SDK, provider abstraction, and configured model without disrupting normal generation?

### RQ2: Reliability and completeness

Does EcoLogits consistently return usable impact values, lifecycle phases, ranges, units, warnings, and errors for representative Research Assistant requests?

### RQ3: Suitability

Are the estimates and their provenance sufficient for:

- Comparing model and response\-length choices
- Communicating per\-response impacts without false precision
- Retaining compatible results for application\-lifetime aggregation

## 3\. Experiment Design

### Experiment 1: Standalone compatibility

Create a standalone compatibility probe using one short, public, non\-sensitive prompt.

Confirm:

- EcoLogits initializes successfully
- The provider client continues to work
- The normal provider response remains available
- An impact object is present
- Token usage remains accessible
- Request latency can be recorded
- Impact values can be read
- Warnings can be read
- Errors can be read

Do not modify the Research Assistant or provider abstraction during this experiment.

Do not store:

- API keys
- Complete prompts
- Generated responses
- Environment\-variable values

#### Purpose

Verify basic compatibility before changing production application code.

### Experiment 2: Configured provider and model

Test the provider and model currently configured by Research Assistant.

Record:

- EcoLogits version
- Provider SDK version
- Provider
- Model
- Model registration status
- Input tokens
- Cached input tokens, if reported
- Output tokens
- Request latency
- Available impact criteria
- Usage\-phase impacts
- Embodied impacts
- Units
- Scalar or range representation
- Warning codes and messages
- Error codes and messages

Do not substitute a different model silently.

If the configured model is unsupported:

1. Record the unsupported result.
2. Preserve the warning or error.
3. Test a supported model only as a separately labeled comparison.
4. Do not attribute the comparison result to the configured model.

### Experiment 3: Controlled Research Assistant requests

Use one fixed research question and the current application configuration:

- Current corpus
- Current Top\-K
- Current system prompt
- Current provider
- Current model
- Temperature set to zero
- Fixed maximum output tokens

Run three requests.

Record:

- Corpus version or corpus fingerprint
- Prompt version
- Retrieval version
- Top\-K
- Retrieved chunk count
- Retrieved\-context size
- Provider
- Model
- Input tokens
- Cached input tokens, if reported
- Output tokens
- Request latency
- Impact criteria
- Usage and embodied phases
- Values or ranges
- Units
- Warnings
- Errors

Do not store the complete question, retrieved evidence, grounded prompt, or generated answer in committed results.

#### Purpose

Determine whether EcoLogits provides consistent, application\-relevant estimates for representative RAG requests.

### Experiment 4: Output\-length comparison

Use the same controlled question and retrieved context with maximum output\-token limits of:

- 100 tokens
- 250 tokens
- 500 tokens

Run each condition once initially. Repeat a condition only if needed to understand an unexpected result and provider cost permits.

Record:

- Maximum\-token setting
- Actual output tokens
- Request latency
- Impact ranges
- Warnings
- Errors
- Whether the response reached the output limit

The human reviewer will evaluate answer completeness and citation preservation outside the sanitized experiment results.

Claude Code must not conclude that the smallest output is the preferred configuration based only on environmental results.

#### Purpose

Evaluate whether response\-length policy offers a practical opportunity to reduce estimated impacts without automatically sacrificing utility.

## 4\. Range, Warning, and Error Handling

EcoLogits results may contain scalar values or ranges.

Preserve:

- Environmental criterion
- Lifecycle phase
- Minimum value
- Maximum value
- Mean value, if supplied
- Unit

Do not calculate or present a midpoint as a measured result.

Warnings and errors are required methodology data.

Preserve:

- Warning or error code
- Warning or error message
- Provider
- Model
- EcoLogits version
- Experiment identifier

A successful provider response does not prove that impact estimation succeeded.

Missing, unsupported, or failed estimates must never be converted to zero.

## 5\. Repetition and Summary Requirements

For repeated conditions, report:

- Valid requests
- Failed requests
- Unsupported requests
- Minimum
- Maximum
- Median
- Arithmetic mean
- Standard deviation
- Coefficient of variation

Calculate descriptive statistics for:

- Request latency
- Input tokens
- Cached input tokens, where available
- Output tokens
- Energy lower and upper bounds
- Global\-warming\-potential lower and upper bounds
- Water lower and upper bounds
- Primary\-energy lower and upper bounds
- Abiotic\-resource\-depletion lower and upper bounds

For ranged values, summarize lower and upper bounds separately.

Claude Code may calculate descriptive statistics. Claude Code must not determine whether variability or uncertainty is acceptable.

## 6\. Output Requirements

Preserve the package\-native impact structure locally.

Also create a sanitized experiment result containing:

- Experiment identifier
- Timestamp
- Git commit
- EcoLogits version
- Provider SDK version
- Provider
- Model
- Request configuration
- Token usage
- Latency
- Retrieved\-context metadata
- Impact criteria
- Lifecycle phases
- Values or ranges
- Units
- Warnings
- Errors
- Execution status

The sanitized result must not contain:

- API keys
- Environment\-variable values
- Complete questions
- Complete prompts
- Retrieved source text
- Generated responses
- Personal information
- Proprietary content

Raw experiment results must remain local and excluded from source control.

## 7\. Repository Access

### Permitted files to inspect

Claude Code may inspect only:

- docs/ecologits\_experiment\_protocol.md
- docs/impact\_accounting\_scope.md
- docs/impact\_decision\_log.md
- CLAUDE.md
- src/sustainability\_rag/\_\_init\_\_.py
- src/sustainability\_rag/config.py
- src/sustainability\_rag/rag\_pipeline.py
- src/sustainability\_rag/resources.py
- src/sustainability\_rag/retrieval.py
- ../pyproject.toml
- ../uv.lock
- ../.gitignore

Claude Code may inspect one additional provider\-related module only if rag\_pipeline.py directly imports that module and it is required to reproduce the existing provider call.

Every additional file inspected must be reported.

### Files and directories not to inspect

Claude Code must not inspect:

- data/markdown/
- data/pdfs/
- notebooks/
- project\_plan.md
- pages/
- Environment\-variable values
- API keys
- Unrelated projects in the parent repository

The restriction against inspecting corpus contents applies to Claude Code repository analysis. It does not prevent the approved experiment script from loading the corpus through initialize\_corpus\_resources() during the controlled RAG experiment.

Claude Code must not substitute synthetic corpus data for the controlled RAG experiment.

## 8\. Permitted Deliverables

Claude Code may create:

- evaluation/test\_ecologits\_integration.py
- evaluation/run\_ecologits\_experiment.py
- evaluation/summarize\_ecologits\_results.py
- evaluation/impact\_results/README.md
- Focused tests for impact extraction, range handling, warning handling, error handling, and result sanitization

Generated local results should use:

- evaluation/impact\_results/ecologits/

Only the directory README should be committed. Raw result files must remain excluded from source control.

## 9\. Implementation Constraints

Claude Code must:

- Begin with a standalone compatibility probe
- Preserve the normal provider response
- Reuse the existing provider and RAG pipeline
- Preserve scalar and range values
- Preserve units
- Preserve usage and embodied phases
- Preserve warnings and errors
- Handle missing or unsupported estimates without crashing
- Keep local retrieval separate from remote inference
- Store only sanitized experiment metadata
- Identify commands that incur provider cost

Claude Code must not:

- Modify Research Assistant during the initial experiment
- Modify the provider abstraction without explicit approval
- Modify retrieval behavior
- Change the configured model silently
- Store prompts or responses
- Add a database
- Add an impact dashboard
- Build a lifetime ledger
- Combine EcoLogits and CodeCarbon values
- Convert missing values to zero
- Classify results as reliable
- Make a paid provider request without explicit authorization

## 10\. Automated Validation

Claude Code may run:

- Python syntax checks
- Script help commands
- Focused unit tests using synthetic impact objects
- Sanitization tests
- Range\-preservation tests
- Warning\- and error\-preservation tests

Claude Code must not make a paid provider request.

The human reviewer will run all real provider experiments.

## 11\. Required Claude Code Report

Claude Code must return:

- Current branch
- Files inspected
- Additional files inspected, if any
- Files created or changed
- Dependency changes
- Commands executed
- Automated validation results
- Manual experiment commands
- Identification of commands that incur provider cost
- Expected result\-file locations
- Known implementation limitations
- Assumptions introduced by the implementation

The report must not interpret environmental estimates or recommend integration.

## 12\. Human Decision Gate

After reviewing the results, the human reviewer will select one outcome.

### Integrate

Use EcoLogits for supported Research Assistant calls.

### Integrate with qualifications

Display estimates with prominent uncertainty, warning, and proprietary\-model disclosures.

### Controlled experiments only

Use EcoLogits for scenario analysis but not per\-response disclosure or lifetime aggregation.

### Use a decoupled EcoLogits API

Use a separate estimation request if SDK instrumentation conflicts with the provider abstraction.

### Supplement

Add a thin application\-owned adapter to connect impact output with interaction, corpus, prompt, and retrieval versions.

### Replace or customize

Develop an application\-specific calculation method only if EcoLogits cannot represent the target provider, model, or RAG characteristics and a defensible alternative methodology can be validated.