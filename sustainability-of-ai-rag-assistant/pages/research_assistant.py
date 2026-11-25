import streamlit as st

from src.sustainability_rag.documents import (
     format_citation,
     clean_section_name,
)
from src.sustainability_rag import fallback
from src.sustainability_rag.resources import initialize_corpus_resources


st.title("Sustainability of AI - Research Assistant")

resources = initialize_corpus_resources()
source_metadata = resources["source_metadata"]
content_chunks = resources["content_chunks"]
embeddings = resources["embeddings"]
metadata_by_id = resources["metadata_by_id"]

PRIVACY_NOTICE = (
    "Gemini free-tier requests should contain only public, non-sensitive information. Do not submit "
    "confidential, personal, client, workplace, or proprietary content. Free-tier content may be used "
    "by Google to improve its products."
)


@st.dialog("Live synthesis is temporarily unavailable")
def fallback_dialog(pending):
    st.write("Gemini is currently unavailable.")
    st.write("Evidence Explorer remains available for retrieving relevant source passages without a "
             "generative-model call.")
    st.write("You may optionally generate this response once with OpenAI. OpenAI is a separate external "
             "provider; choosing this option sends the grounded request (your question and the retrieved "
             "source passages) to OpenAI.")
    open_col, openai_col, cancel_col = st.columns(3)
    if open_col.button("Open Evidence Explorer"):
        st.switch_page("pages/evidence_explorer.py")
    if openai_col.button("Generate once with OpenAI"):
        with st.spinner("Generating with OpenAI..."):
            fallback.confirm_openai(st.session_state, pending, content_chunks, embeddings)
        st.rerun()
    if cancel_col.button("Cancel"):
        fallback.cancel(st.session_state)
        st.rerun()


st.caption(PRIVACY_NOTICE)
question = st.text_input("Ask a question about the environmental impacts of AI").strip()

if question:
    response = fallback.run_primary(st.session_state, question, content_chunks, embeddings)
    pending = fallback.take_pending(st.session_state)
    if pending:
        fallback_dialog(pending)  # at most one dialog per script run
    if response is None:
        st.info(fallback.UNAVAILABLE_MESSAGE)
        if st.session_state.get("fallback_failed"):
            st.warning("OpenAI is also unavailable right now.")
        st.page_link("pages/evidence_explorer.py", label="Open Evidence Explorer")
        if st.button("Try Gemini again"):
            fallback.retry_primary(st.session_state)
            st.rerun()
    else:
        if response["provider"] != "gemini":
            st.caption(f"Generated once with {response['provider']} after your confirmation.")
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
