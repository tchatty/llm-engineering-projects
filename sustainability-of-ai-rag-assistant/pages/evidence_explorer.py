import streamlit as st
from src.sustainability_rag.config import EMBEDDING_MODEL_NAME
from src.sustainability_rag.resources import initialize_corpus_resources
from src.sustainability_rag.retrieval import search_evidence

st.title("Evidence Explorer")
st.markdown(
    """
    Search the curated research corpus and inspect the most semantically relevant paper sections directly.
    
    This page uses a sentence-embedding model for retrieval and does **NOT** call a generative large language model or generate a summary. 
    """
)


resources = initialize_corpus_resources()
source_metadata = resources["source_metadata"]
metada_by_id = resources["metadata_by_id"]
content_chunks = resources["content_chunks"]
embeddings = resources["embeddings"]


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





