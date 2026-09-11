"""
ingest_documents.py
Splits the .txt documents in data/documents/ into chunks matching the
schema Person 1 requested: document_id, component, failure_type, text, source.
Writes the result to data/documents/chunks.json.
"""

import os
import csv
import json

DOCS_DIR = os.path.join("data", "documents")
METADATA_CSV = os.path.join(DOCS_DIR, "documents_metadata.csv")
OUTPUT_JSON = os.path.join(DOCS_DIR, "chunks.json")
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

# filename -> (document_id, component, failure_type)
# component/failure_type are the primary subsystem/fault each document covers,
# used so retrieved evidence can be matched against a case's component/failure.
DOCUMENT_INFO = {
    "hydraulic_troubleshooting_guide.txt": ("DOC-001", "General", "General"),
    "hydraulic_filter_sop.txt": ("DOC-002", "Hydraulic Filter", "Filter blockage"),
    "cooling_system_sop.txt": ("DOC-003", "Oil Cooler", "Cooler restriction"),
}


def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + size
        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break
        start += size - overlap
    return chunks


def ingest():
    all_chunks = []
    for fname, (doc_id, component, failure_type) in DOCUMENT_INFO.items():
        path = os.path.join(DOCS_DIR, fname)
        if not os.path.exists(path):
            print(f"WARNING: {path} not found, skipping")
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for chunk in chunk_text(text):
            all_chunks.append({
                "document_id": doc_id,
                "component": component,
                "failure_type": failure_type,
                "text": chunk,
                "source": fname,
            })

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Wrote {len(all_chunks)} chunks from {len(DOCUMENT_INFO)} documents to {OUTPUT_JSON}")


if __name__ == "__main__":
    ingest()
