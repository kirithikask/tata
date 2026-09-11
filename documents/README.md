# Data — Engineering Memory Prototype

## Sources
- `machines.csv`, `maintenance_cases.csv` — synthetic demo data authored for
  this prototype. NOT real Tata Hitachi maintenance records.
- `documents/*.txt` — prototype SOPs/guides written for demo purposes, each
  labeled "PROTOTYPE DEMO DOCUMENT" at the top of the file.
- `documents/documents_metadata.csv` — metadata (id, title, type, subsystem,
  version, date, status) for each document above.

## Limitations
- Small sample size (25 cases) — not statistically representative of real
  fleet history.
- Symptom phrasing is manually varied to aid semantic retrieval, not drawn
  from real technician logs.
- Similarity/evidence scores produced downstream by the retrieval engine are
  retrieval-based, not calibrated probabilities.
- The UCI hydraulic dataset, if used by the optional sensor model, is a
  test-rig benchmark and not excavator-specific data.

## Files
| File | Purpose |
|---|---|
| `machines.csv` | Machine registry (3 demo excavators) |
| `maintenance_cases.csv` | 25 historical case records — the core retrieval source for Person 1's engine |
| `documents/*.txt` | SOP/guide text, chunked for evidence retrieval |
| `documents/documents_metadata.csv` | Metadata for each document |
| `documents/chunks.json` | Output of `scripts/ingest_documents.py` — chunked document text with metadata |
| `scripts/ingest_documents.py` | Splits documents into overlapping chunks, writes `chunks.json` |
| `scripts/build_doc_index.py` | Optional — builds a FAISS index over document chunks |
| `scripts/quality_check.py` | Validates ID integrity, duplicates, missing fields |

## How to run
```bash
pip install pandas --break-system-packages
python data/scripts/quality_check.py
python data/scripts/ingest_documents.py
# optional, requires faiss-cpu + sentence-transformers:
python data/scripts/build_doc_index.py
```

## Failure categories covered in maintenance_cases.csv
Pump leakage, cooler restriction, filter blockage, valve problems,
accumulator pressure loss, oil contamination, cylinder leakage, pilot
pressure problems, line restriction — 2–3 cases each.
