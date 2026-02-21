# Quick Start Guide - ML Model Repository

## 🚀 Fast Setup (3 Steps)

### Option 1: Full Version (Python 3.8+)

#### 1. Install Dependencies

```bash
pip install sentence-transformers faiss-cpu transformers torch numpy
```

**Note**: If you get version errors, try:
```bash
pip install sentence-transformers==2.0.0 faiss-cpu==1.7.3 transformers==4.18.0 torch==1.11.0 numpy==1.21.6
```

#### 2. Build the Index

```bash
python model.py
```

This downloads the embedding model (~80MB) and creates the FAISS index.

#### 3. Test It

```bash
python rag_pipeline.py
```

Type your agricultural questions and get AI-powered answers!

### Option 2: Simple Version (Python 3.7+)

#### 1. Install Dependencies

```bash
pip install scikit-learn numpy
```

#### 2. Build the Index

```bash
python model_simple.py
```

This creates TF-IDF vectors (no model downloads).

#### 3. Test It

```bash
python rag_simple.py
```

Type your agricultural questions and get template-based answers!

## 📝 Example Queries

- "My paddy has brown spots. What to do?"
- "How to control pests in cotton?"
- "When should I apply urea fertilizer?"
- "My plants have yellow leaves. What's wrong?"

## 🔧 Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'faiss'`
**Solution**: Use simple version: `python model_simple.py` (no FAISS needed)

**Problem**: `ModuleNotFoundError: No module named 'sentence_transformers'`
**Solution**: Use simple version or install: `pip install sentence-transformers`

**Problem**: `ModuleNotFoundError: No module named 'sklearn'`
**Solution**: `pip install scikit-learn`

**Problem**: Version conflicts
**Solution**: Use Python 3.8+ for full version, or Python 3.7+ for simple version

**Problem**: Unicode errors on Windows
**Solution**: Files updated to avoid emoji - should work now

## ✅ Verify Installation

Run the test suite:
```bash
python run_tests.py
```

Or test manually:
```bash
# Test simple version (always works)
python model_simple.py
python query_simple.py
python rag_simple.py
```

## 🎯 Which Version to Use?

- **Full Version**: Better accuracy, requires Python 3.8+ and more dependencies
- **Simple Version**: Works with Python 3.7+, no model downloads, faster setup

Both versions work! Choose based on your Python version and needs.

## 📚 Next Steps

- Add more documents to `data.py`
- Integrate with main KrishiSahay backend
- Upgrade to better LLM models
- Add multilingual support
- Fine-tune on agricultural data
