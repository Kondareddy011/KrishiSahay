"""
Build Embeddings + Simple Vector Search (No FAISS required)
Works with Python 3.7+ and basic dependencies
"""

import numpy as np
import pickle
import os

# Try to use sentence-transformers, fallback to basic if not available
try:
    from sentence_transformers import SentenceTransformer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("sentence-transformers not available - using basic TF-IDF")

if HAS_TRANSFORMERS:
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
else:
    print("Using basic TF-IDF vectorization...")
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        HAS_SKLEARN = True
    except ImportError:
        HAS_SKLEARN = False
        print("⚠️  sklearn not available - install: pip install scikit-learn")

# Load data
from data import documents

print(f"Loaded {len(documents)} documents")

os.makedirs("models", exist_ok=True)

if HAS_TRANSFORMERS:
    # Convert documents to embeddings
    print("Converting documents to embeddings...")
    doc_embeddings = model.encode(documents, show_progress_bar=True)
    
    print(f"Embeddings shape: {doc_embeddings.shape}")
    
    # Save embeddings
    with open("models/embeddings.npy", "wb") as f:
        np.save(f, doc_embeddings)
    print("Saved embeddings to models/embeddings.npy")
    
elif HAS_SKLEARN:
    # Use TF-IDF as fallback
    print("Creating TF-IDF vectors...")
    vectorizer = TfidfVectorizer(max_features=100)
    doc_embeddings = vectorizer.fit_transform(documents).toarray()
    
    with open("models/embeddings.npy", "wb") as f:
        np.save(f, doc_embeddings)
    
    with open("models/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    print("Saved TF-IDF vectors")
else:
    print("No vectorization method available")
    doc_embeddings = None

# Save documents list
with open("models/documents.pkl", "wb") as f:
    pickle.dump(documents, f)
print("Saved documents to models/documents.pkl")

print("\nModel building complete!")
print("Run 'python query_simple.py' to test queries")
