import re
import json

from .config import DATA_DIR, SOURCE_METADATA_PATH


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

def load_source_metadata():
    if not SOURCE_METADATA_PATH.exists(): 
        raise FileNotFoundError(f"Source metadata file not found:" f"{SOURCE_METADATA_PATH}")
    with SOURCE_METADATA_PATH.open(encoding="utf-8") as f:
        sources = json.load(f)
    validate_source_metadata(sources)
    return sources

REQUIRED_SOURCE_FIELDS = {
    "id", "filename", "title", "author", "issued"
}

def validate_source_metadata(sources):
    if not isinstance(sources, list):
        raise ValueError("Source metadata must be a json array")

    source_ids = []
    filenames = []
    
    for index, source in enumerate(sources, start=1):
        missing_fields = (
            REQUIRED_SOURCE_FIELDS - source.keys()
        )

        if missing_fields:
            raise ValueError(
                f"Metadata record {index} is missing: "
                f"{sorted(missing_fields)}"
            )

        if not source["id"]:
            raise ValueError(
                f"Metadata record {index} has no source ID."
            )

        if not source["filename"]:
            raise ValueError(
                f'{source["id"]} has no filename.'
            )

        if not source["title"]:
            raise ValueError(
                f'{source["id"]} has no paper title.'
            )

        if not isinstance(source["author"], list):
            raise ValueError(
                f'{source["id"]} author must be a list.'
            )

        if not source["author"]:
            raise ValueError(
                f'{source["id"]} has no authors.'
            )

        date_parts = (
            source.get("issued", {})
            .get("date-parts", [])
        )

        if not date_parts or not date_parts[0]:
            raise ValueError(
                f'{source["id"]} has no publication date.'
            )

        source_ids.append(source["id"])
        filenames.append(source["filename"])

    if len(source_ids) != len(set(source_ids)):
        raise ValueError(
            "Duplicate source IDs found in sources.json."
        )

    if len(filenames) != len(set(filenames)):
        raise ValueError(
            "Duplicate filenames found in sources.json."
        )

def build_source_registry(source_metadata):
    return {
        source["filename"] : source["id"]
        for source in source_metadata
    }


def validate_corpus_metadata(docs, metadata_by_filename):
    doc_files = {doc["source"] for doc in docs}
    metadata_files = set(metadata_by_filename)

    missing_metadata = sorted(doc_files - metadata_files)
    if missing_metadata:
        raise ValueError(
            f"Markdown documents with no metadata record: {missing_metadata}"
        )

    missing_docs = sorted(metadata_files - doc_files)
    if missing_docs:
        raise ValueError(
            f"Metadata records with no Markdown document: {missing_docs}"
        )


def format_author_name(author):
    return author.get("family") or author.get("literal") or ""


def format_citation(reference):
    #Lightweight display citation: Family (Year). Title.
    names = [format_author_name(a) for a in reference["author"]]
    if len(names) == 1:
        author_text = names[0]
    elif len(names) == 2:
        author_text = f"{names[0]} and {names[1]}"
    else:
        author_text = f"{names[0]} et al."
    year = reference["issued"]["date-parts"][0][0]
    title = reference["title"].rstrip()
    if title[-1] not in ".?!":
        title += "."
    return f"{author_text} ({year}). {title}"


def clean_section_name(section):
    return section.lstrip("#").strip()


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
