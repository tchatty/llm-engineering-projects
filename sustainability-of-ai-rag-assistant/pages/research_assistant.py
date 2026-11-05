import streamlit as st

from src.sustainability_rag.documents import (
     format_citation,
     clean_section_name,
)
# from src.sustainability_rag.embeddings import embed_chunks
from src.sustainability_rag.resources import initialize_corpus_resources
from src.sustainability_rag.rag_pipeline import answer_question


st.title("Sustainability of AI - Research Assistant")

resources = initialize_corpus_resources()
source_metadata = resources["source_metadata"]
content_chunks = resources["content_chunks"]
embeddings = resources["embeddings"]
metadata_by_id = resources["metadata_by_id"]
#content_chunks, embeddings, metadata_by_id = load_knowledge_base()

question = st.text_input("Ask a question about the environmental impacts of AI")

if question:
    response = answer_question(question, content_chunks, embeddings)
    st.write(response["answer"])
    st.subheader("Sources Used")
    for source_id, info in response["source_map"].items():
        source_metadata = metadata_by_id.get(source_id)
        if source_metadata is None:
            st.markdown(f"**[{source_id}]** Metadata unavailable")
        else:
            citation = format_citation(source_metadata)
            st.markdown(f"**[{source_id}]** {citation}")

        for section in info["sections"]:
            section_name = clean_section_name(section)
            st.markdown(f"- Section: {section_name}")
