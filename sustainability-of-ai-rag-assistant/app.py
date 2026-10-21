# Navigation router. Run from the project root with: uv run streamlit run app.py
import streamlit as st

st.set_page_config(page_title="Sustainability of AI", layout="wide")

pages = [
    st.Page("pages/research_assistant.py", title="Research Assistant", default=True),
    st.Page("pages/evidence_explorer.py", title="Evidence Explorer"),
    st.Page("pages/research_briefs.py", title="Research Briefs"),
    st.Page("pages/knowledge_graph.py", title="Knowledge Graph"),
    st.Page("pages/sources.py", title="Sources"),
    st.Page("pages/impact_methodology.py", title="Impact & Methodology"),
]

with st.sidebar:
    st.subheader("Resource-Aware Design")
    st.caption("Design principles and planned capabilities; not all are implemented yet.")
    st.markdown(
        "- Evidence-first retrieval\n"
        "- Reviewed research briefs\n"
        "- Response caching\n"
        "- Small-model defaults\n"
        "- Impact transparency"
    )

st.navigation(pages).run()
