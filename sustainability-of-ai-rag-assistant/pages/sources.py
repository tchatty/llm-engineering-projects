import streamlit as st

from src.sustainability_rag.documents import load_source_metadata, format_citation

st.title("Sources")

for source in load_source_metadata():
    st.markdown(f"**[{source['id']}]** {format_citation(source)}")
    if source.get("container-title"):
        st.caption(source["container-title"])
    if source.get("DOI"):
        st.markdown(f"DOI: [{source['DOI']}](https://doi.org/{source['DOI']})")
    if source.get("URL"):
        st.markdown(f"URL: [{source['URL']}]({source['URL']})")
    st.divider()
