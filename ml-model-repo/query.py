"""
Query + Retrieval System
Searches agricultural knowledge base using FAISS
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle

# Load model
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load documents
try:
    with open("models/documents.pkl", "rb") as f:
        documents = pickle.load(f)
    print(f"✅ Loaded {len(documents)} documents")
except FileNotFoundError:
    print("⚠️  Documents file not found. Loading from data.py...")
    from data import documents

# Load or create FAISS index
if os.path.exists("models/agricultural_index.faiss"):
    print("Loading FAISS index...")
    index = faiss.read_index("models/agricultural_index.faiss")
    print(f"✅ Loaded index with {index.ntotal} documents")
else:
    print("⚠️  Index not found. Creating new index...")
    dimension = 384
    index = faiss.IndexFlatL2(dimension)
    
    print("Encoding documents...")
    doc_embeddings = model.encode(documents)
    index.add(np.array(doc_embeddings, dtype='float32'))
    
    os.makedirs("models", exist_ok=True)
    faiss.write_index(index, "models/agricultural_index.faiss")
    print(f"✅ Created and saved index with {index.ntotal} documents")


def search(query: str, top_k: int = 3):
    """
    Search agricultural knowledge base
    
    Args:
        query: User's question
        top_k: Number of results to return
        
    Returns:
        List of relevant documents
    """
    # Convert query to embedding
    query_vector = model.encode([query])
    
    # Search FAISS index
    distances, indices = index.search(np.array(query_vector, dtype='float32'), k=top_k)
    
    # Retrieve relevant documents
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(documents):
            results.append({
                "document": documents[idx],
                "distance": float(distances[0][i]),
                "rank": i + 1
            })
    
    return results


def search_simple(query: str, top_k: int = 3):
    """Simple search returning just document strings"""
    results = search(query, top_k)
    return [r["document"] for r in results]


if __name__ == "__main__":
    # Test queries
    test_queries = [
        "My paddy has brown spots. What to do?",
        "How to control pests in cotton?",
        "When to apply urea fertilizer?",
        "What causes yellow leaves?"
    ]
    
    print("\n" + "="*60)
    print("🔍 Testing Query System")
    print("="*60 + "\n")
    
    for query_text in test_queries:
        print(f"Query: {query_text}")
        print("-" * 60)
        
        results = search(query_text, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. (Distance: {result['distance']:.4f})")
            print(f"   {result['document']}")
        
        print("\n" + "="*60 + "\n")
