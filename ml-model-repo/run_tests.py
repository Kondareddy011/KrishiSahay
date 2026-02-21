"""
Test script for ML Model Repository
Tests all components: data loading, indexing, querying, and RAG
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Install: pip install sentence-transformers faiss-cpu transformers torch numpy")
        return False

def test_data():
    """Test data loading"""
    print("\n📚 Testing data loading...")
    try:
        from data import documents
        print(f"✅ Loaded {len(documents)} documents")
        return True
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_query():
    """Test query system"""
    print("\n🔍 Testing query system...")
    try:
        from query import search
        results = search("pest control", top_k=2)
        if results:
            print(f"✅ Query successful - found {len(results)} results")
            return True
        else:
            print("⚠️  Query returned no results")
            return False
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False

def test_rag():
    """Test RAG pipeline"""
    print("\n🤖 Testing RAG pipeline...")
    try:
        from rag_pipeline import generate_answer
        answer = generate_answer("How to control pests?", use_llm=False)
        if answer:
            print("✅ RAG pipeline working")
            print(f"   Sample answer: {answer[:100]}...")
            return True
        else:
            print("⚠️  RAG returned empty answer")
            return False
    except Exception as e:
        print(f"❌ RAG error: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🧪 ML Model Repository - Test Suite")
    print("="*60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Data Loading", test_data()))
    results.append(("Query System", test_query()))
    results.append(("RAG Pipeline", test_rag()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        sys.exit(1)
