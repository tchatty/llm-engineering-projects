import streamlit as st


st.title("Sustainability of AI")

st.markdown(
    """
    ### Evidence-first research on the environmental impacts of AI

    This application helps users explore research on the environmental
    impacts of artificial intelligence. It prioritizes direct access to
    evidence before using generative AI to synthesize an answer.
    """
)

st.info(
    "Recommended journey: inspect the evidence first, then use the "
    "Research Assistant when synthesis across sources would add value."
)

st.divider()


# ---------------------------------------------------------------------
# Objectives
# ---------------------------------------------------------------------

st.header("Objectives")

st.markdown(
    """
    This project is designed to:

    - Make reviewed research easier to find and examine.
    - Distinguish retrieved evidence from generated synthesis.
    - Avoid live LLM calls when retrieval or reviewed content is sufficient.
    - Develop transparent methods for tracking the application's impacts.
    """
)

st.divider()


# ---------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------

st.header("Explore the application")

feature_columns = st.columns(2)

with feature_columns[0]:
    with st.container(border=True):
        st.subheader("Evidence Explorer")
        st.markdown(
            """
            Find relevant sections in the curated research corpus without
            making a generative LLM call.

            **Recommended starting point.**
            """
        )
        st.page_link(
            "pages/evidence_explorer.py",
            label="Open Evidence Explorer",
            icon="🔎",
            use_container_width=True,
        )

with feature_columns[1]:
    with st.container(border=True):
        st.subheader("Research Assistant")
        st.markdown(
            """
            Generate a grounded synthesis using evidence retrieved from
            the research corpus.

            **Use when synthesis adds value.**
            """
        )
        st.page_link(
            "pages/research_assistant.py",
            label="Open Research Assistant",
            icon="💬",
            use_container_width=True,
        )

feature_columns = st.columns(2)

with feature_columns[0]:
    with st.container(border=True):
        st.subheader("Research Briefs")
        st.markdown(
            """
            Read authored analyses that compare findings, examine
            uncertainty, and discuss decision implications.
            """
        )
        st.page_link(
            "pages/research_briefs.py",
            label="View Research Briefs",
            icon="📄",
            use_container_width=True,
        )

with feature_columns[1]:
    with st.container(border=True):
        st.subheader("Knowledge Graph")
        st.markdown(
            """
            Explore relationships between research papers and a manually
            curated vocabulary of sustainability topics.
            """
        )
        st.page_link(
            "pages/knowledge_graph.py",
            label="Open Knowledge Graph",
            icon="🔗",
            use_container_width=True,
        )

st.divider()


# ---------------------------------------------------------------------
# Impact methodology
# ---------------------------------------------------------------------

st.header("Impact assessment methodology")

st.caption("Under development")

st.markdown(
    """
    This section will describe how the application uses CodeCarbon and
    EcoLogits to assess impacts associated with local computation,
    retrieval, and remote LLM calls.

    The methodology will also explain system boundaries, assumptions,
    uncertainty, and which application activities can or cannot be
    meaningfully compared.
    """
)

st.page_link(
    "pages/impact_methodology.py",
    label="View Impact & Methodology",
    icon="📊",
)

st.divider()


# ---------------------------------------------------------------------
# Limitations
# ---------------------------------------------------------------------

st.header("Limitations")

st.markdown(
    """
    - The curated corpus does not represent all available research.
    - Semantic similarity measures relevance, not scientific quality,
      correctness, confidence, or completeness.
    - Generated answers depend on the evidence retrieved for the question.
    - Users should review the original publications before making
      consequential decisions.
    - Application-level environmental impact tracking is not yet implemented.
    """
)

st.divider()


# ---------------------------------------------------------------------
# Call to action
# ---------------------------------------------------------------------

st.subheader("Start with the evidence")

st.page_link(
    "pages/evidence_explorer.py",
    label="Explore the research corpus",
    icon="🔎",
    use_container_width=True,
)