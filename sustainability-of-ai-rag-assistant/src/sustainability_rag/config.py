from pathlib import Path

# Project root is two levels up from this file: <root>/src/sustainability_rag/config.py
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "markdown"
TOP_K = 5
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

#Active Model Configuration
PROVIDER = "openai"  # Change this to "anthropic", "openrouter", or "ollama" as needed
MODELS = {
    "openai": "gpt-4.1-mini",
    "anthropic": "claude-sonnet-5-5",
    "openrouter": "openrouter/free",
    "ollama": "llama3.2"
}
