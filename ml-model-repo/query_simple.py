"""
Simple Query + Retrieval System (No FAISS required)
Uses numpy for cosine similarity search
"""

import numpy as np
import pickle
import os

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Try to load model
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        HAS_SKLEARN = True
    except ImportError:
        HAS_SKLEARN = False

# Load documents
try:
    with open("models/documents.pkl", "rb") as f:
        documents = pickle.load(f)
    print(f"Loaded {len(documents)} documents")
except FileNotFoundError:
    print("⚠️  Documents file not found. Loading from data.py...")
    from data import documents

# Load embeddings
if os.path.exists("models/embeddings.npy"):
    doc_embeddings = np.load("models/embeddings.npy")
    print(f"Loaded embeddings: {doc_embeddings.shape}")
else:
    print("Embeddings not found. Run 'python model_simple.py' first")
    doc_embeddings = None

if HAS_SKLEARN and os.path.exists("models/vectorizer.pkl"):
    with open("models/vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)


def search(query: str, top_k: int = 3):
    """
    Search agricultural knowledge base using cosine similarity
    
    Args:
        query: User's question
        top_k: Number of results to return
        
    Returns:
        List of relevant documents with similarity scores
    """
    if doc_embeddings is None:
        return []
    
    # Convert query to embedding
    if HAS_TRANSFORMERS:
        query_vector = model.encode([query])[0]
    elif HAS_SKLEARN:
        query_vector = vectorizer.transform([query]).toarray()[0]
    else:
        print("No vectorization method available")
        return []
    
    # Calculate cosine similarities
    similarities = []
    for i, doc_emb in enumerate(doc_embeddings):
        sim = cosine_similarity(query_vector, doc_emb)
        similarities.append((i, sim))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return top_k results
    results = []
    for i, (idx, sim) in enumerate(similarities[:top_k]):
        results.append({
            "document": documents[idx],
            "similarity": float(sim),
            "rank": i + 1
        })
    
    return results


if __name__ == "__main__":
    # Test queries
    test_queries = [
        "My paddy has brown spots. What to do?",
        "How to control pests in cotton?",
        "When to apply urea fertilizer?",
        "What causes yellow leaves?"
    ]
    
    print("\n" + "="*60)
    print("Testing Query System")
    print("="*60 + "\n")
    
    for query_text in test_queries:
        print(f"Query: {query_text}")
        print("-" * 60)
        
        results = search(query_text, top_k=2)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"\n{i}. (Similarity: {result['similarity']:.4f})")
                print(f"   {result['document']}")
        else:
            print("No results found")
        
        print("\n" + "="*60 + "\n")
