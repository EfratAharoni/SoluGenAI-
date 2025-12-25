"""
Retrieval Module
Handles querying the vector database and returning relevant results
"""

import chromadb
import config

class RetrieverError(Exception):
    """Custom exception for retrieval errors"""
    pass

class Retriever:
    def __init__(self):
        """
        Initialize the retriever with ChromaDB
        """
        try:
            self.client = chromadb.PersistentClient(path=config.CHROMA_DIR)
            self.collection = self.client.get_collection(name=config.COLLECTION_NAME)
            
            # Load local embedding model
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
        except Exception as e:
            raise RetrieverError(f"Failed to initialize retriever: {e}")
    
    def retrieve(self, query, top_k=None, threshold=None):
        """
        Retrieve relevant documents for a query
        
        Args:
            query (str): User query
            top_k (int): Number of results to return (default: from config)
            threshold (float): Minimum similarity score (default: from config)
        
        Returns:
            list: List of dicts with 'id', 'text', 'score', 'metadata'
        """
        if not query or not query.strip():
            raise RetrieverError("Query cannot be empty")
        
        top_k = top_k or config.TOP_K
        threshold = threshold if threshold is not None else config.SIMILARITY_THRESHOLD
        
        try:
            # Create query embedding using local model
            query_embedding = self.model.encode([query.strip()])[0].tolist()
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "distances", "metadatas"]
            )
            
            # Format results
            formatted_results = []
            
            if results and results['documents'] and len(results['documents'][0]) > 0:
                for i in range(len(results['documents'][0])):
                    # Convert distance to similarity score
                    distance = results['distances'][0][i]
                    similarity = 1 / (1 + distance)
                    
                    # Apply threshold
                    if similarity >= threshold:
                        formatted_results.append({
                            'id': results['ids'][0][i],
                            'text': results['documents'][0][i],
                            'score': round(similarity, 4),
                            'distance': round(distance, 4),
                            'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                        })
            
            return formatted_results
        
        except Exception as e:
            raise RetrieverError(f"Retrieval failed: {e}")

# Singleton instance
_retriever = None

def get_retriever():
    """
    Get or create retriever instance
    """
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever

def retrieve(query, top_k=None, threshold=None):
    """
    Convenience function for retrieval
    """
    retriever = get_retriever()
    return retriever.retrieve(query, top_k, threshold)