from pathlib import Path

# Project root is two levels up from this file: <root>/src/sustainability_rag/config.py
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "markdown"
SOURCE_METADATA_PATH = Path(__file__).resolve().parents[2] / "data" / "metadata" / "sources.json"
TOP_K = 5
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Provider configuration (single source of truth)
DEFAULT_PROVIDER = "gemini"   # Used for every request unless a provider is passed explicitly
FALLBACK_PROVIDER = "openai"  # Never called automatically; only after explicit user confirmation
MODELS = {
    "gemini": "gemini-3.5-flash-lite",  # validated free-tier model (see docs/ecologits_gemini_experiment_findings.md)
    "openai": "gpt-4o-mini",            # cheapest OpenAI model validated with EcoLogits
    "anthropic": "claude-sonnet-5-5",
    "openrouter": "openrouter/free",
    "ollama": "llama3.2",
}
MAX_OUTPUT_TOKENS = 500
