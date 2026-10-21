import numpy as np

from .config import TOP_K
from .embeddings import generate_embeddings


#Create a function for semantic retrieval of relevant chunks based on the query
def retrieve_relevant_chunks(query, content_chunks, embeddings, top_k=TOP_K):
    query_embedding = generate_embeddings([query])[0]
    query_embedding = query_embedding / np.linalg.norm(query_embedding)  # Normalize query embedding
    similarities = embeddings @ query_embedding  # Compute cosine similarity using dot product
    top_chunks = np.argsort(similarities)[-top_k:][::-1]
    #score = np.strip(similarities[top_chunks])
    return [(content_chunks[i], similarities[i]) for i in top_chunks]


def build_context(results):
    context_blocks = []

    for rank, (chunk, score) in enumerate(results, start=1):
        context_block = f"""[{chunk['source_id']}]Source: {chunk['source']}\nSection: {chunk['section']}\nText: {chunk['text']}""".strip()
        context_blocks.append(context_block)

    return "\n\n".join(context_blocks)
