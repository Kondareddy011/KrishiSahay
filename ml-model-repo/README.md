# Agricultural RAG Pipeline - ML Model Repository

A Retrieval-Augmented Generation (RAG) system for agricultural question answering using vector search and LLM generation.

## 🚀 Features

- **Vector Search**: FAISS-based semantic search (or numpy-based for Python 3.7)
- **Embeddings**: Sentence Transformers for document encoding (or TF-IDF fallback)
- **RAG Pipeline**: Combines retrieval with LLM generation
- **Simple Version**: Works with Python 3.7+ without FAISS/transformers
- **Multilingual Support**: Works with Indian languages (can be extended)

## 📋 Requirements

### Full Version (Python 3.8+)

```bash
pip install sentence-transformers faiss-cpu transformers torch numpy
```

### Simple Version (Python 3.7+)

```bash
pip install scikit-learn numpy
```

The simple version uses TF-IDF instead of embeddings and numpy cosine similarity instead of FAISS.

## 🏗️ Project Structure

```
ml-model-repo/
├── data.py              # Agricultural knowledge dataset (20 documents)
├── model.py             # Build FAISS index + embeddings (full version)
├── query.py             # Query and retrieval system (full version)
├── rag_pipeline.py      # Full RAG pipeline with LLM (full version)
├── model_simple.py      # Simple version (TF-IDF, no FAISS)
├── query_simple.py      # Simple query (numpy cosine similarity)
├── rag_simple.py        # Simple RAG (template-based, no LLM)
├── setup.py             # Setup script
├── run_tests.py         # Test suite
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── QUICKSTART.md       # Quick start guide
└── .gitignore          # Git ignore file
```

## 📚 Step-by-Step Usage

### Option 1: Full Version (Python 3.8+)

#### Step 1: Install Requirements

```bash
pip install sentence-transformers faiss-cpu transformers torch numpy
```

#### Step 2: Build FAISS Index

```bash
python model.py
```

This will:
- Load embedding model (`all-MiniLM-L6-v2`)
- Convert documents to embeddings
- Create FAISS index
- Save to `models/` directory

#### Step 3: Test Query System

```bash
python query.py
```

Tests the retrieval system with sample queries.

#### Step 4: Run RAG Pipeline

```bash
python rag_pipeline.py
```

Runs the full RAG pipeline with LLM answer generation.

### Option 2: Simple Version (Python 3.7+)

#### Step 1: Install Requirements

```bash
pip install scikit-learn numpy
```

#### Step 2: Build Index

```bash
python model_simple.py
```

This will:
- Create TF-IDF vectors
- Save to `models/` directory

#### Step 3: Test Query System

```bash
python query_simple.py
```

#### Step 4: Run RAG Pipeline

```bash
python rag_simple.py
```

Runs template-based RAG (no LLM required).

## 🔍 Example Usage

### Full Version

```python
from query import search
from rag_pipeline import generate_answer

# Simple search
results = search("How to control pests in rice?", top_k=3)
for r in results:
    print(f"{r['rank']}. {r['document']} (distance: {r['distance']:.4f})")

# Full RAG answer
answer = generate_answer("My paddy has brown spots. What to do?")
print(answer)
```

### Simple Version

```python
from query_simple import search
from rag_simple import generate_answer

# Simple search
results = search("How to control pests in rice?", top_k=3)
for r in results:
    print(f"{r['rank']}. {r['document']} (similarity: {r['similarity']:.4f})")

# Template-based answer
answer = generate_answer("My paddy has brown spots. What to do?")
print(answer)
```

## 🎯 Output Example

**Query**: "My paddy crop has brown spots. What should I do?"

**Answer (Full Version)**:
```
Based on agricultural best practices:

Brown spots on paddy leaves indicate fungal infection. Use carbendazim fungicide.

Additional information:
- Monitor crops weekly for early pest and disease detection.
- Apply appropriate organic pesticides (neem oil, garlic-chili spray).
```

**Answer (Simple Version)**:
```
Based on agricultural best practices:

Brown spots on paddy leaves indicate fungal infection. Use carbendazim fungicide.

Additional information:
- PM-KISAN scheme provides financial support to farmers.
```

## ⚡ Upgrade Ideas

1. **Better LLM**: Replace `distilgpt2` with:
   - Mistral 7B (via Ollama)
   - LLaMA 2/3
   - GPT-3.5/4 (via API)

2. **Multilingual Models**: 
   - Use IndicBERT for Hindi/Telugu
   - mBERT for multilingual support

3. **Voice Integration**: 
   - Add Whisper for speech-to-text
   - Text-to-speech for answers

4. **Real Dataset**: 
   - Use Kaggle agricultural datasets
   - KVK (Krishi Vigyan Kendra) knowledge base
   - Government agricultural schemes data

5. **Fine-tuning**: 
   - Fine-tune on Indian agricultural data
   - Domain-specific embeddings

## 🔧 Configuration

Edit `data.py` to add more agricultural knowledge documents.

Modify `rag_pipeline.py` to change LLM model or generation parameters.

## 📝 Notes

- **Full Version**: First run downloads models (~500MB)
- **Simple Version**: No model downloads, works immediately
- FAISS index is saved for faster subsequent runs
- GPU acceleration available if CUDA is installed
- Falls back to template-based generation if LLM unavailable

## 🤝 Integration

This ML model can be integrated with the main KrishiSahay backend:

```python
# In backend/main.py or separate service
from rag_pipeline import generate_answer  # Full version
# Or:
from rag_simple import generate_answer     # Simple version

# In your API endpoint
answer = generate_answer(user_query)
```

## 🧪 Testing

Run the test suite:

```bash
python run_tests.py
```

Or test individual components:

```bash
# Test data loading
python -c "from data import documents; print(len(documents))"

# Test query (full version)
python query.py

# Test query (simple version)
python query_simple.py

# Test RAG (full version)
python rag_pipeline.py

# Test RAG (simple version)
python rag_simple.py
```

## 📄 License

Part of KrishiSahay project.

## 🔗 Related Documentation

- Main project: `../README.md`
- Setup guide: `../SETUP.md`
- Quick start: `QUICKSTART.md`
