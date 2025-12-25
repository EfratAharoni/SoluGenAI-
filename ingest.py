"""
Data Ingestion Script
Loads restaurant reviews, creates embeddings, and stores them in ChromaDB
"""

import pandas as pd
import chromadb
from openai import OpenAI
import config
import sys

def chunk_text(text, chunk_size, overlap):
    """
    Split text into overlapping chunks
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def load_data():
    """
    Load and validate the dataset
    """
    try:
        df = pd.read_csv(config.DATA_PATH)
        
        if config.TEXT_COLUMN not in df.columns:
            raise ValueError(f"Column '{config.TEXT_COLUMN}' not found in CSV")
        
        # Clean data
        df = df[[config.TEXT_COLUMN]].dropna()
        df[config.TEXT_COLUMN] = df[config.TEXT_COLUMN].astype(str).str.strip()
        
        # Remove empty reviews
        df = df[df[config.TEXT_COLUMN].str.len() > 0]
        
        texts = df[config.TEXT_COLUMN].tolist()
        
        print(f"✓ Loaded {len(texts)} reviews")
        print(f"✓ Average length: {sum(len(t) for t in texts) / len(texts):.0f} chars")
        print(f"✓ Sample review: {texts[0][:100]}...")
        
        return texts
    
    except FileNotFoundError:
        print(f"❌ Error: File not found at {config.DATA_PATH}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)

def prepare_documents(texts):
    """
    Optionally chunk texts if they're very long
    """
    if config.USE_CHUNKING:
        print(f"✓ Chunking texts (size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP})")
        all_chunks = []
        chunk_to_review_map = []
        
        for idx, text in enumerate(texts):
            chunks = chunk_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
            for chunk in chunks:
                all_chunks.append(chunk)
                chunk_to_review_map.append(idx)
        
        print(f"✓ Created {len(all_chunks)} chunks from {len(texts)} reviews")
        return all_chunks, chunk_to_review_map
    else:
        print(f"✓ Using full reviews (no chunking)")
        return texts, list(range(len(texts)))

def create_embeddings(documents):
    """
    Create embeddings using sentence-transformers (FREE, LOCAL)
    """
    try:
        print(f"✓ Loading local embedding model...")
        from sentence_transformers import SentenceTransformer
        
        # Use free local model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print(f"✓ Creating embeddings for {len(documents)} documents...")
        vectors = model.encode(documents, show_progress_bar=True)
        vectors = [v.tolist() for v in vectors]
        
        print(f"✓ Created {len(vectors)} embeddings")
        return vectors
    
    except ImportError:
        print("❌ Please install: pip install sentence-transformers")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating embeddings: {e}")
        sys.exit(1)

def store_in_chromadb(documents, vectors, metadata_map):
    """
    Store documents and embeddings in ChromaDB
    """
    try:
        # Initialize ChromaDB
        client = chromadb.PersistentClient(path=config.CHROMA_DIR)
        
        # Delete existing collection if it exists
        try:
            client.delete_collection(name=config.COLLECTION_NAME)
            print(f"✓ Deleted existing collection")
        except:
            pass
        
        # Create new collection
        collection = client.create_collection(
            name=config.COLLECTION_NAME,
            metadata={"description": "Restaurant reviews embeddings"}
        )
        
        # Prepare IDs and metadata
        ids = [f"doc_{i}" for i in range(len(documents))]
        metadatas = [{"review_idx": idx} for idx in metadata_map]
        
        # Add to collection
        collection.add(
            documents=documents,
            embeddings=vectors,
            ids=ids,
            metadatas=metadatas
        )
        
        print(f"✓ Stored {len(documents)} documents in ChromaDB")
        print(f"✓ Collection: {config.COLLECTION_NAME}")
        print(f"✓ Location: {config.CHROMA_DIR}")
        
    except Exception as e:
        print(f"❌ Error storing in ChromaDB: {e}")
        sys.exit(1)

def main():
    """
    Main ingestion pipeline
    """
    print("\n" + "="*50)
    print("🚀 RAG Ingestion Pipeline")
    print("="*50 + "\n")
    
    # Step 1: Load data
    print("[1/4] Loading data...")
    texts = load_data()
    
    # Step 2: Prepare documents
    print(f"\n[2/4] Preparing documents...")
    documents, metadata_map = prepare_documents(texts)
    
    # Step 3: Create embeddings
    print(f"\n[3/4] Creating embeddings...")
    vectors = create_embeddings(documents)
    
    # Step 4: Store in ChromaDB
    print(f"\n[4/4] Storing in ChromaDB...")
    store_in_chromadb(documents, vectors, metadata_map)
    
    print("\n" + "="*50)
    print("✅ Ingestion completed successfully!")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()