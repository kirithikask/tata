"""
build_doc_index.py
OPTIONAL - only run this if time permits.
Builds a FAISS index over the document chunks produced by ingest_documents.py,
using the same embedding model Person 1 uses for case retrieval
(BAAI/bge-small-en-v1.5) so both indexes are comparable.

Requires: pip install faiss-cpu sentence-transformers numpy
"""

import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

CHUNKS_JSON = os.path.join("data", "documents", "chunks.json")
INDEX_OUT = os.path.join("models", "document_chunks.faiss")
METADATA_OUT = os.path.join("models", "document_chunks_metadata.json")


def build():
    with open(CHUNKS_JSON, encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        print("No chunks found - run ingest_documents.py first.")
        return

    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(np.array(embeddings, dtype="float32"))

    os.makedirs("models", exist_ok=True)
    faiss.write_index(index, INDEX_OUT)

    with open(METADATA_OUT, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"Indexed {len(chunks)} chunks -> {INDEX_OUT}")


if __name__ == "__main__":
    build()
