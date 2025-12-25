# RAG Retrieval System – Restaurant Reviews

A semantic search system for restaurant reviews based on a Retrieval-Augmented Generation (RAG-style) architecture. The system enables natural-language search over restaurant reviews using local embeddings and a vector database.

---

## Project Overview

**Purpose**
Enable semantic search over 300 Yelp restaurant reviews using free, local embedding models instead of keyword-based matching.

**Functionality**

* Accepts natural language queries
* Retrieves the most semantically similar reviews
* Ranks results by similarity score

**Motivation**
Keyword search fails to capture meaning (e.g., "good service" vs. "staff was amazing").
Semantic embeddings address this by representing meaning rather than exact words.

---

## System Architecture

User Query
→ Local SentenceTransformer Embedding (query vector)
→ ChromaDB semantic search (Top-K retrieval)
→ Flask backend and UI for result display

---

## Technology Stack

**Note:** Although the assignment specified using OpenAI embeddings (text-embedding-3-small), I encountered a payment processing constraint (no compatible credit card available within the deadline). To deliver a fully functional end-to-end RAG system, I implemented the solution using a local Sentence-Transformers embedding model and documented the trade-offs.

* **Embeddings**: SentenceTransformer `all-MiniLM-L6-v2` (local, free)
* **Vector Database**: ChromaDB
* **Backend / API**: Flask
* **Language**: Python 3.9+

The system does **not** use OpenAI APIs. All embeddings are generated locally with no cost and no external data transfer.

---

## Dataset

* **Source**: Yelp restaurant reviews (Kaggle)
* **Size**: 300 reviews (slightly above assignment requirement for better semantic variety)
* **Use Case**: Real-world restaurant feedback (e.g., ice cream quality, service, vegan options)

**Fields Used**

* Review Text (primary content)
* Rating, Date, URL (metadata)

**Data Preparation**

* Removed empty or null reviews
* Deduplicated entries
* Average review length: ~600 characters
* Chunking not applied (reviews are short and self-contained)

---

## Setup and Installation

**Requirements**

* Python 3.9+

**Installation**

```bash
git clone 
cd rag-restaurant-reviews
pip install -r requirements.txt
```

**Data Ingestion**

```bash
python ingest.py
```

Expected output:

* 300 reviews loaded
* 300 embeddings created (dimension: 384)
* Data stored in ChromaDB

**Run Application**

```bash
python app.py
```

Access via: [http://localhost:5000](http://localhost:5000)


---
# Project Demo

[Watch the demo video here]([https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing](https://drive.google.com/file/d/1tJOrTsioQQdfE2qdG61nixhKZ12CID_4/view?usp=sharing))


---

## Usage

**Web Interface**

* Enter a natural language query
* View Top-K most similar reviews with similarity scores

**API Example**

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "matcha ice cream", "top_k": 3}'
```

**Python Example**

```python
from retrieve import retrieve
results = retrieve("best ice cream flavors")
for r in results:
    print(r["score"], r["text"][:100])
```

---

## Configuration

File: `config.py`

* `TOP_K = 5`
  Number of retrieved results per query

* `SIMILARITY_THRESHOLD = 0.5`
  Minimum similarity score (0–1)

* `EMBEDDING_MODEL = "all-MiniLM-L6-v2"`
  Local SentenceTransformer model (free, no API)

---

## Embedding Model Rationale

**Model Used**: `sentence-transformers/all-MiniLM-L6-v2`

**Reasons**

* No usage cost
* No API latency
* Full data privacy (runs locally)
* Sufficient quality for small-to-medium datasets

---

## Testing Summary

Sample query results:

* "ice cream flavors" → similarity ~0.87
* "slow service complaints" → similarity ~0.82
* "vegan options" → similarity ~0.79

Average query latency: ~120ms

**Edge Case Handling**

* Empty queries return a user-friendly error
* Very long queries are truncated
* No-match queries return an empty result set

---

## Design Decisions

* No Chunking: Reviews are short enough to embed as full documents
* ChromaDB: Lightweight, persistent, no server or API key required
* L2 Distance converted to normalized similarity score (0–1)
* Flask chosen for simplicity and extensibility
* Similarity Scoring: > ChromaDB by default uses L2 (Euclidean) distance. Since the assignment requires a similarity score (typically 0 to 1), I applied the formula 1 / (1 + distance). This ensures that a distance of 0 (identical) results in a score of 1, and as the distance increases, the score approaches 0.

---

## Known Limitations

* Dataset limited to 300 reviews
* No re-ranking stage
* No caching
* Single collection only

---

## Future Improvements

* Metadata filtering
* Query caching
* Cross-encoder re-ranking
* Hybrid keyword + semantic search
* Full RAG generation layer

---

## Security Notes

* No external APIs used
* Input validation applied
* No authentication or rate limiting

---

## Author

Efrat Aharoni

---
