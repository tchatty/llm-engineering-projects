import streamlit as st
from src.sustainability_rag.config import EMBEDDING_MODEL_NAME
from src.sustainability_rag.documents import (
    build_source_registry, 
    chunk_by_section,
    load_documents,
    load_source_metadata,
    validate_corpus_metadata,    
)
from src.sustainability_rag.embeddings import embed_chunks
from src.sustainability_rag.retrieval import search_evidence

st.title("Evidence Explorer")
st.markdown(
    """
    Search the curated research corpus and inspect the most semantically relevant paper sections directly.
    
    This page uses a sentence-embedding model for retrieval and does **NOT** call a generative large language model or generate a summary. 
    """
)

@st.cache_resource
def initialize_evidence_search():
    """
    Load the corpus and prepare reusable retrieval resources.
    Streamlit caches the returned resources so they are not rebuilt on every page interaction.
    """

    source_metadata = load_source_metadata()
    metadata_by_id = {
        source["id"]: source
        for source in source_metadata
    }

    metadata_by_filename = {
        source["filename"]: source
        for source in source_metadata
    }

    source_registry = build_source_registry(source_metadata)

    docs = load_documents()
    validate_corpus_metadata(docs, metadata_by_filename)

    all_chunks = []
    for doc in docs:
        all_chunks.extend(
            chunk_by_section(
                doc, source_registry,
            )
        )

    content_chunks = [
        chunk
        for chunk in all_chunks
        if chunk["type"] == "content"
    ]

    embeddings = embed_chunks(content_chunks)

    return {
        "source_metadata": source_metadata,
        "metadata_by_id": metadata_by_id,
        "content_chunks": content_chunks,
        "embeddings": embeddings,
    }

resources = initialize_evidence_search()

with st.form("evidence_search_form"):
    question = st.text_input(
        "What would you like to investigate?",
        placeholder="For example: How do the impacts of inference compare to training?"
    )

    result_count = st.selectbox(
        "Number of evidence sections",
        options=[3, 5],
        index=0,
    )

    submitted = st.form_submit_button(
        "Search evidence",
        type="primary",
    )

if submitted:
    if not question.strip():
        st.warning(
            "Enter a question or topic before searching."
        )
    else:
        with st.spinner(
            "Searching the research corpus..."
        ):
            evidence_results = search_evidence(
                query = question,
                content_chunks=resources["content_chunks"],
                embeddings=resources["embeddings"],
                metadata_by_id=resources["metadata_by_id"],
                top_k=result_count,
            )

        st.subheader("Search Details")

        detail_columns = st.columns(4)
        detail_columns[0].metric(
            "Response pathway",
            "Evidence only",
        )

        detail_columns[1].metric(
            "Generative LLM",
            "Not used",
        )

        detail_columns[2].metric(
            "Sections searched",
            len(resources["content_chunks"]),
        )

        detail_columns[3].metric(
            "Results shown",
            len(evidence_results),
        )

        st.caption(
            f"Embedding model: `{EMBEDDING_MODEL_NAME}`"
        )

        st.info(
            "Results are ranked by semantic similarity."
            "Similarity indicates how closely a section aligns"
            "with the question in the embedding space. It does"
            "not measure research quality, scientific certainty," 
            "correctness, or completeness."
        )

        st.subheader("Relevant evidence")

        for result in evidence_results:
            label = (
                f'{result["rank"]}. '
                f'[{result["source_id"]}] '
                f'{result["section"]} · '
                f'Similarity {result["similarity"]:.3f}'
            )

            with st.expander(
                label,
                expanded=False,
            ):
                st.markdown(
                    f'**{result["citation"]}**'
                )
                st.markdown(
                    f'**Section:** {result["section"]}'
                )

                st.markdown(
                    f'**Semantic similarity:** '
                    f'{result["similarity"]:.3f}'
                )

                if result.get("url"):
                    st.link_button(
                        "Open publication",
                        result["url"],
                    )

                st.divider()

                st.markdown("**Retrieved evidence**")

                st.markdown(result["text"])

        st.warning(
            "These are the nearest matches in the current "
            "curated corpus. Their inclusion does not "
            "necessarily mean that the corpus contains a "
            "complete answer to the question."
        )





