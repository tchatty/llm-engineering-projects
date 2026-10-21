import streamlit as st

from src.sustainability_rag.documents import (
    load_documents,
    load_source_metadata,
    build_source_registry,
    validate_corpus_metadata,
    chunk_by_section,
    format_citation,
    clean_section_name,
)
from src.sustainability_rag.embeddings import embed_chunks
from src.sustainability_rag.rag_pipeline import answer_question


@st.cache_resource
def load_knowledge_base():
    source_metadata = load_source_metadata()
    metadata_by_filename = {s["filename"]: s for s in source_metadata}
    metadata_by_id = {s["id"]: s for s in source_metadata}
    docs = load_documents()
    validate_corpus_metadata(docs, metadata_by_filename)
    source_registry = build_source_registry(source_metadata)
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_by_section(doc, source_registry))
    content_chunks = [chunk for chunk in all_chunks if chunk["type"] == "content"]
    embeddings = embed_chunks(content_chunks)
    return content_chunks, embeddings, metadata_by_id


st.title("Sustainability of AI - Research Assistant")

content_chunks, embeddings, metadata_by_id = load_knowledge_base()

question = st.text_input("Ask a question about the environmental impacts of AI")

if question:
    response = answer_question(question, content_chunks, embeddings)
    st.write(response["answer"])
    st.subheader("Sources Used")
    for source_id, info in response["source_map"].items():
        st.markdown(f"**[{source_id}]** {format_citation(metadata_by_id[source_id])}")
        for section in info["sections"]:
            st.markdown(f"- Section: {clean_section_name(section)}")
