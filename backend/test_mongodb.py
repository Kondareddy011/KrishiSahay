"""
Test script for MongoDB integration.
Verifies connection and basic CRUD operations.
"""
import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from database import Database

def test_mongodb():
    print("Testing MongoDB Integration...")
    
    # Load env
    load_dotenv()
    
    # Check if MongoDB URI is set
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("FAIL: MONGODB_URI not found in .env")
        return

    # Initialize database
    db = Database()
    
    if db.mongodb is None:
        print("FAIL: MongoDB client not initialized. Is MongoDB running?")
        return
        
    print("SUCCESS: Connected to MongoDB")
    
    # Test caching
    query = "test query " + str(os.urandom(4).hex())
    answer = "test answer"
    category = "Test Category"
    
    print(f"Caching response for query: {query}")
    db.cache_response(query, "en", answer, category)
    
    # Retrieve from cache
    print("Retrieving from cache...")
    cached = db.get_cached_response(query, "en")
    
    if cached and cached["answer"] == answer:
        print("SUCCESS: Cache retrieval works!")
    else:
        print(f"FAIL: Cache retrieval failed. Got: {cached}")
        
    # Test feedback
    print("Saving feedback...")
    db.save_feedback(query, answer, "helpful")
    
    # Test app feedback
    print("Saving app feedback...")
    db.save_app_feedback("Great app!", 5, "test_page")
    
    # Test recent feedback retrieval
    print("Retrieving recent feedback...")
    recent = db.get_recent_app_feedback(limit=5)
    if any(f.get("message") == "Great app!" for f in recent):
        print("SUCCESS: App feedback retrieval works!")
    else:
        print("FAIL: App feedback retrieval failed.")

if __name__ == "__main__":
    test_mongodb()
