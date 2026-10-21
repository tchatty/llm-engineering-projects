import re

from .config import DATA_DIR


#Defining a function to load documents from the specified data directory
def load_documents():
    assert DATA_DIR.exists(), f"Data directory not found: {DATA_DIR}"
    docs = []

    for file in DATA_DIR.glob("*.md"):
        docs.append({
            "source": file.name,
            "content": file.read_text(encoding="utf-8")
        })
    return docs


def build_source_registry(docs):
    return {
        doc["source"]: f"S{i}"
        for i, doc in enumerate(
            sorted(docs, key=lambda d: d["source"]),
            start=1
        )
    }


def chunk_by_section(doc, source_registry):
    #Split the markdown text into sections based on headings into retrieval friendly chunks

    sections = re.split(r'(?=^##)', doc["content"], flags=re.MULTILINE)
    chunks = []
    for section_text in sections:
        section_text = section_text.strip()
        if not section_text:
            continue

        section_name = section_text.splitlines()[0].strip()  # Get the first line as the section name

        body_text = "\n".join(section_text.splitlines()[1:]).strip()  # Get the rest of the section as the body text

        #skip the title and metadata block
        if section_name.startswith("# "):
            continue

        if not body_text:
            continue
        #Tag chunks for future filtering based on section type
        if section_name == "## Executive Summary":
            chunk_type = "executive_summary"
        elif section_name == "## Abstract":
            chunk_type = "abstract"
        elif section_name == "## References":
            chunk_type = "references"
        else:
            chunk_type = "content"

        chunks.append({
            "source_id": source_registry[doc["source"]],
            "source": doc["source"],
            "section": section_name,
            "text": body_text,
            "type": chunk_type
        })
    return chunks
