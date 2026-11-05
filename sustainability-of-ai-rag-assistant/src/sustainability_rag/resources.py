"""Shared corpus resources for the streamlit application"""

import streamlit as st
from .documents import (
    build_source_registry,
    chunk_by_section,
    load_documents,
    load_source_metadata,
    validate_corpus_metadata,
)

from .embeddings import embed_chunks

@st.cache_resource
def initialize_corpus_resources():
    """Load, chunk, and embed the corpus once per Streamlit process"""
    source_metadata = load_source_metadata()
    metadata_by_id = {
        source["id"]: source
        for source in source_metadata
    }

    metadata_by_filename = {
        source["filename"]: source
        for source in source_metadata
    }

    documents = load_documents()

    validate_corpus_metadata(documents,metadata_by_filename)
    source_registry = build_source_registry(source_metadata)
    all_chunks =[]

    for document in documents:
        document_chunks = chunk_by_section(document, source_registry)
        all_chunks.extend(document_chunks)

    content_chunks = [
        chunk
        for chunk in all_chunks if chunk["type"] == "content"
    ]

    embeddings = embed_chunks(content_chunks)

    return {
        "source_metadata": source_metadata,
        "metadata_by_id": metadata_by_id,
        "content_chunks": content_chunks,
        "embeddings": embeddings,
    }