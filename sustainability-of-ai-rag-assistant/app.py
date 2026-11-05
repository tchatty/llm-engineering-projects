# Navigation router. Run from the project root with: uv run streamlit run app.py
import streamlit as st

st.set_page_config(page_title="Sustainability of AI", layout="wide")

pages = [
    st.Page("pages/home.py", title="Start Here", icon=":material/home:", default=True),
    st.Page("pages/evidence_explorer.py", title="Evidence Explorer", icon=":material/search:"),
    st.Page("pages/research_assistant.py", title="Research Assistant", icon=":material/psychology:"),
    st.Page("pages/research_briefs.py", title="Research Briefs", icon=":material/article:"),
    st.Page("pages/knowledge_graph.py", title="Knowledge Graph", icon=":material/hub:"),
    st.Page("pages/sources.py", title="Sources", icon=":material/library_books:"),
    st.Page("pages/impact_methodology.py", title="Impact & Methodology", icon=":material/monitoring:"),
]

with st.sidebar:
    st.subheader("Evidence-First Research")
    st.caption("Use the least resource-intensive pathway to meet your research needs.")
    st.markdown(
        "1. **Retrieve** evidence\n"
        "2. **Review** authored research\n"
        "3. **Reuse** valid cached content\n"
        "4. **Generate** only when useful\n"
        "5. **Measure and disclose** supported impacts"
    )

st.divider()

st.caption("Environmental-impact accounting is under development. "
        "No application-lifetime impact totals are currently reported.")

st.navigation(pages).run()
