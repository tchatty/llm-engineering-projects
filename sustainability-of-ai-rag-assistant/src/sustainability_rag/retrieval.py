import numpy as np

from .config import TOP_K
from .embeddings import generate_embeddings
from .documents import format_citation, clean_section_name


#Create a function for semantic retrieval of relevant chunks based on the query
def retrieve_relevant_chunks(query, content_chunks, embeddings, top_k=TOP_K):
    query_embedding = generate_embeddings([query])[0]
    query_embedding = query_embedding / np.linalg.norm(query_embedding)  # Normalize query embedding
    similarities = embeddings @ query_embedding  # Compute cosine similarity using dot product
    top_chunks = np.argsort(similarities)[-top_k:][::-1]
    return [(content_chunks[i], similarities[i]) for i in top_chunks]


def build_context(results):
    context_blocks = []

    for rank, (chunk, score) in enumerate(results, start=1):
        context_block = f"""[{chunk['source_id']}]Source: {chunk['source']}\nSection: {chunk['section']}\nText: {chunk['text']}""".strip()
        context_blocks.append(context_block)

    return "\n\n".join(context_blocks)

def search_evidence(
        query,
        content_chunks,
        embeddings,
        metadata_by_id,
        top_k=3,
):
    """
    Retrieve relevant corpus sections and attach citation metadata. This function performs retrieval only with no LLM calls
    """
    if not query or not query.strip():
        return[]
    
    results = retrieve_relevant_chunks(
        query=query,
        content_chunks=content_chunks,
        embeddings=embeddings,
        top_k=top_k,
    )
    evidence_results = []
    for rank, (chunk,score) in enumerate(results, start=1):
        source_id = chunk["source_id"]
        if source_id not in metadata_by_id:
            raise KeyError(f"Source metadata not found for {source_id}")
        reference = metadata_by_id[source_id]
        evidence_results.append(
            {
                "rank": rank,
                "source_id": source_id,
                "citation": format_citation(reference),
                "section": clean_section_name(chunk["section"]),
                "similarity": float(score),
                "text": chunk["text"],
                "url": reference.get("URL"),
                "doi": reference.get("DOI"),
            }
        )

    return evidence_results