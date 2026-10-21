import numpy as np
from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL_NAME

_embedding_model = None


def get_embedding_model():
    # Load the model on first use (not at import time) and reuse it afterwards
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedding_model


#Create a function to generate embeddings for the text chunks
def generate_embeddings(text_chunks):
    embeddings = get_embedding_model().encode(text_chunks, convert_to_numpy=True)
    return embeddings


def embed_chunks(chunks):
    embeddings = generate_embeddings([chunk["text"] for chunk in chunks])
    return embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)  # Normalize embeddings
