"""
RAG Pipeline with FAISS vector search and LLM integration
"""

import os
import json
import numpy as np
from typing import Dict, List, Optional
from sentence_transformers import SentenceTransformer
import faiss

class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline for agricultural queries.
    Uses FAISS for fast vector similarity search.
    """
    
    def __init__(self, index_path: str = None, data_path: str = None):
        _base = os.path.dirname(os.path.abspath(__file__))
        self.index_path = index_path or os.path.join(_base, "faiss_index", "agricultural_index.faiss")
        self.data_path = data_path or os.path.join(_base, "data", "agricultural_knowledge.json")
        self.index = None
        self.documents = []
        self.embeddings = None
        self.model = None
        self.index_loaded = False
        
    def load_index(self):
        """Load FAISS index and documents"""
        try:
            # Load sentence transformer model
            print("Loading embedding model...")
            self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
            
            # Load documents
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                print(f"Loaded {len(self.documents)} documents")
            else:
                print(f"Warning: Data file not found at {self.data_path}")
                self.documents = []
            
            # Load FAISS index
            if os.path.exists(self.index_path) and len(self.documents) > 0:
                self.index = faiss.read_index(self.index_path)
                print(f"Loaded FAISS index with {self.index.ntotal} vectors")
                self.index_loaded = True
            else:
                print("FAISS index not found. Please run setup_faiss.py first.")
                self.index_loaded = False
                
        except Exception as e:
            print(f"Error loading index: {e}")
            self.index_loaded = False
    
    def query(self, query: str, top_k: int = 3) -> Dict:
        """
        Query the RAG pipeline and return answer
        
        Args:
            query: User's question
            top_k: Number of relevant documents to retrieve
            
        Returns:
            Dictionary with answer and metadata
        """
        if not self.index_loaded or not self.index:
            # Fallback to mock response
            return self._generate_mock_response(query)
        
        try:
            # Convert query to embedding
            query_embedding = self.model.encode([query])
            query_embedding = np.array(query_embedding, dtype='float32')
            
            # Search FAISS index
            distances, indices = self.index.search(query_embedding, top_k)
            
            # Retrieve relevant documents
            relevant_docs = []
            for idx in indices[0]:
                if idx < len(self.documents):
                    relevant_docs.append(self.documents[idx])
            
            # Generate answer using context
            answer = self._generate_answer(query, relevant_docs)
            category = self._detect_category(query, relevant_docs)
            
            return {
                "answer": answer,
                "category": category,
                "sources": [doc.get("title", "") for doc in relevant_docs[:3]]
            }
            
        except Exception as e:
            print(f"Error in RAG query: {e}")
            return self._generate_mock_response(query)
    
    def _generate_answer(self, query: str, context_docs: List[Dict]) -> str:
        """
        Generate answer using retrieved context and LLM (or mock)
        """
        # Combine context
        context = "\n\n".join([
            f"{doc.get('title', '')}\n{doc.get('content', '')}"
            for doc in context_docs
        ])
        
        # Simple template-based generation (replace with actual LLM in production)
        # For now, return the most relevant document's content
        if context_docs:
            best_match = context_docs[0]
            answer = best_match.get("content", "")
            
            # Format as agricultural advice
            if answer:
                return self._format_agricultural_answer(query, answer)
        
        return self._generate_mock_response(query)["answer"]
    
    def _format_agricultural_answer(self, query: str, content: str) -> str:
        """Format answer as practical agricultural advice"""
        # Extract key information and format it
        lines = content.split('\n')
        formatted = []
        
        for line in lines[:10]:  # Limit to first 10 lines
            if line.strip():
                formatted.append(line.strip())
        
        answer = "\n".join(formatted)
        
        # Add practical tone
        if not answer.startswith("To"):
            answer = f"To address your question about '{query}':\n\n{answer}"
        
        return answer
    
    def _detect_category(self, query: str, docs: List[Dict]) -> Optional[str]:
        """Detect category from query and documents"""
        query_lower = query.lower()
        
        categories = {
            "Crops & Cultivation": ["plant", "crop", "cultivate", "sow", "harvest", "rice", "wheat", "cotton"],
            "Pest Management": ["pest", "insect", "disease", "control", "aphid", "borer"],
            "Fertilizers": ["fertilizer", "npk", "urea", "nutrient", "manure"],
            "Government Schemes": ["scheme", "pm-kisan", "insurance", "credit", "subsidy"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return "General Agriculture"
    
    def _generate_mock_response(self, query: str) -> Dict:
        """Generate mock response when RAG is unavailable"""
        query_lower = query.lower()
        
        # Simple keyword-based responses
        mock_responses = {
            "rice": "Rice cultivation requires well-drained soil with pH 5-6.5. Plant during monsoon season (June-July). Use 20-25 kg seeds per hectare. Apply NPK fertilizer (100:50:50 kg/ha) in split doses. Maintain 5-7 cm water depth during growth.",
            "pest": "For pest control, use integrated pest management (IPM). Identify pests early. Use neem-based organic pesticides as first line of defense. Rotate crops to break pest cycles. Maintain field hygiene.",
            "fertilizer": "Apply fertilizers based on soil test results. For most crops, NPK ratio of 4:2:1 works well. Apply nitrogen in split doses - 50% at sowing, 25% at tillering, 25% at flowering. Use organic compost to improve soil health.",
            "wheat": "Wheat grows best in loamy soil with pH 6-7.5. Sow in November-December. Use 100-125 kg seeds per hectare. Apply 120 kg N, 60 kg P2O5, 40 kg K2O per hectare. Harvest when grains are hard and moisture is 20-25%."
        }
        
        for key, response in mock_responses.items():
            if key in query_lower:
                return {
                    "answer": response,
                    "category": self._detect_category(query, []),
                    "sources": []
                }
        
        return {
            "answer": f"Thank you for your question about '{query}'. For detailed agricultural advice, please consult your local agricultural extension officer or visit the nearest Krishi Vigyan Kendra (KVK). They can provide region-specific guidance based on your soil type and climate conditions.",
            "category": "General Agriculture",
            "sources": []
        }
