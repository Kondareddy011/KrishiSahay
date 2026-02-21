"""
Quick test script to verify backend API is working
Run this after starting the backend server
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_ask():
    """Test /ask endpoint"""
    print("Testing /ask endpoint...")
    payload = {
        "query": "How to grow rice?",
        "language": "en"
    }
    response = requests.post(f"{BASE_URL}/ask", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_feedback():
    """Test /feedback endpoint"""
    print("Testing /feedback endpoint...")
    payload = {
        "query": "How to grow rice?",
        "answer": "Rice cultivation requires...",
        "feedback": "positive"
    }
    response = requests.post(f"{BASE_URL}/feedback", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    try:
        print("=" * 50)
        print("KrishiSahay Backend API Test")
        print("=" * 50)
        print()
        
        test_health()
        test_ask()
        test_feedback()
        
        print("=" * 50)
        print("All tests completed!")
        print("=" * 50)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to backend server.")
        print("Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")
