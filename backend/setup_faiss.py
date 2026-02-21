"""
Setup script to create FAISS index from agricultural knowledge base
Run this script once to build the vector index
"""

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

def create_faiss_index():
    """Create FAISS index from agricultural knowledge base"""
    _base = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(_base, "data", "agricultural_knowledge.json")
    
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        print("Please ensure agricultural_knowledge.json exists")
        return
    
    with open(data_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    print(f"Loaded {len(documents)} documents")
    
    # Initialize sentence transformer model
    print("Loading embedding model...")
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    # Generate embeddings
    print("Generating embeddings...")
    texts = []
    for doc in documents:
        # Combine title and content for embedding
        text = f"{doc.get('title', '')} {doc.get('content', '')}"
        texts.append(text)
    
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings, dtype='float32')
    
    print(f"Generated embeddings shape: {embeddings.shape}")
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance
    
    # Add embeddings to index
    print("Building FAISS index...")
    index.add(embeddings)
    
    # Save index
    index_path = os.path.join(_base, "faiss_index")
    os.makedirs(index_path, exist_ok=True)
    
    index_file = os.path.join(index_path, "agricultural_index.faiss")
    faiss.write_index(index, index_file)
    
    print(f"FAISS index saved to {index_file}")
    print(f"Index contains {index.ntotal} vectors")
    print("Setup complete!")

if __name__ == "__main__":
    create_faiss_index()
