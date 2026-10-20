# Placeholder Streamlit app. Run from the project root with: streamlit run app.py
import streamlit as st

from src.sustainability_rag.documents import load_documents, build_source_registry, chunk_by_section
from src.sustainability_rag.embeddings import embed_chunks
from src.sustainability_rag.rag_pipeline import answer_question


@st.cache_resource
def load_knowledge_base():
    docs = load_documents()
    source_registry = build_source_registry(docs)
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_by_section(doc, source_registry))
    content_chunks = [chunk for chunk in all_chunks if chunk["type"] == "content"]
    embeddings = embed_chunks(content_chunks)
    return content_chunks, embeddings


st.title("Sustainability of AI - Research Assistant")

content_chunks, embeddings = load_knowledge_base()

question = st.text_input("Ask a question about the environmental impacts of AI")

if question:
    response = answer_question(question, content_chunks, embeddings)
    st.write(response["answer"])
    st.subheader("Sources Used")
    for source_id, info in response["source_map"].items():
        st.write(f"{source_id}: {info['source']} (Section: {info['section']})")
