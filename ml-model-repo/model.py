"""
Build FAISS Index + Embedding Model
Creates vector embeddings and FAISS index for agricultural documents
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle

# Load embedding model (better model for multilingual support)
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions, fast and efficient

# Load data
from data import documents

print(f"Loaded {len(documents)} documents")

# Convert documents to embeddings
print("Converting documents to embeddings...")
doc_embeddings = model.encode(documents, show_progress_bar=True)

print(f"Embeddings shape: {doc_embeddings.shape}")

# Create FAISS index
dimension = doc_embeddings.shape[1]  # 384 for all-MiniLM-L6-v2
index = faiss.IndexFlatL2(dimension)  # L2 distance (Euclidean)

# Add embeddings to index
print("Adding embeddings to FAISS index...")
index.add(np.array(doc_embeddings, dtype='float32'))

print(f"✅ FAISS index created with {index.ntotal} documents")
print(f"   Dimension: {dimension}")
print(f"   Index type: {type(index).__name__}")

# Save index and model for later use
os.makedirs("models", exist_ok=True)

# Save FAISS index
faiss.write_index(index, "models/agricultural_index.faiss")
print("✅ Saved FAISS index to models/agricultural_index.faiss")

# Save documents list
with open("models/documents.pkl", "wb") as f:
    pickle.dump(documents, f)
print("✅ Saved documents to models/documents.pkl")

# Save embeddings (optional, for faster loading)
with open("models/embeddings.npy", "wb") as f:
    np.save(f, doc_embeddings)
print("✅ Saved embeddings to models/embeddings.npy")

print("\n🎉 Model building complete!")
print("   Run 'python query.py' to test queries")
