# AI Coding Agent Instructions for RAG Restaurant Reviews System

## Architecture Overview
This is a Retrieval-Augmented Generation (RAG) system for semantic search over restaurant reviews. It uses local embeddings (sentence-transformers/all-MiniLM-L6-v2) stored in ChromaDB, with a Flask web UI and API.

**Data Flow:**
1. `ingest.py` loads CSV data, creates embeddings, stores in ChromaDB
2. `app.py` serves web UI and API endpoints
3. `retrieve.py` handles queries by embedding input and finding similar reviews

**Key Components:**
- **No chunking**: Reviews are short (~600 chars), stored as full documents
- **Similarity scoring**: `similarity = 1 / (1 + distance)` converts L2 distance to 0-1 score
- **Singleton retriever**: `get_retriever()` ensures one ChromaDB connection

## Essential Patterns
- **Error handling**: Use `RetrieverError` for query failures, catch in Flask routes
- **Configuration**: All settings in `config.py` (TOP_K=5, THRESHOLD=0.5, etc.)
- **Embedding model**: Local `all-MiniLM-L6-v2` for cost-free operation (OpenAI config is placeholder)
- **Metadata**: Each document has `review_idx` mapping back to original CSV row

## Developer Workflows
- **Ingest data**: `python ingest.py` (loads `data/Restaurant Reviews.csv`, creates embeddings)
- **Run app**: `python app.py` (starts Flask on :5000)
- **Query API**: POST `/api/search` with `{"query": "text", "top_k": 5, "threshold": 0.5}`
- **Test retrieval**: `from retrieve import retrieve; results = retrieve("ice cream")`

## Code Examples
**Query with custom params:**
```python
results = retrieve("slow service", top_k=3, threshold=0.7)
for r in results:
    print(f"Score: {r['score']:.2f} | {r['text'][:50]}...")
```

**API response format:**
```json
{
  "query": "ice cream",
  "results": [{"id": "doc_0", "text": "...", "score": 0.87, "metadata": {"review_idx": 0}}],
  "count": 1
}
```

**Config changes:** Edit `config.py` for TOP_K, THRESHOLD, or switch to OpenAI embeddings (requires updating `retrieve.py` and `ingest.py`).

## Key Files
- [`config.py`](config.py): All configuration constants
- [`retrieve.py`](retrieve.py): Core retrieval logic and singleton
- [`app.py`](app.py): Flask routes with embedded HTML template
- [`ingest.py`](ingest.py): Data loading and ChromaDB storage</content>
<parameter name="filePath">c:\Users\EFRAT\Desktop\SoluGenAI‏\.github\copilot-instructions.md