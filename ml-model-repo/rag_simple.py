"""
Simple RAG Pipeline (No FAISS/LLM required)
Uses template-based answer generation
"""

from query_simple import search


def generate_answer(query: str) -> str:
    """
    Generate answer using simple RAG pipeline
    
    Args:
        query: User's question
        
    Returns:
        Generated answer
    """
    # Step 1: Retrieve relevant context
    results = search(query, top_k=3)
    
    if not results:
        return "I couldn't find relevant information. Please consult your local agricultural extension officer."
    
    # Step 2: Generate answer from top results
    top_result = results[0]['document']
    
    # Format as answer
    answer = f"Based on agricultural best practices:\n\n{top_result}"
    
    # Add additional context if available
    if len(results) > 1:
        answer += f"\n\nAdditional information:\n"
        for r in results[1:]:
            answer += f"- {r['document']}\n"
    
    return answer


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Simple RAG Pipeline - Agricultural Q&A")
    print("="*60 + "\n")
    
    # Test questions
    test_questions = [
        "My paddy crop has brown spots. What should I do?",
        "How can I control pests in my cotton field?",
        "When should I apply urea fertilizer?",
        "My plants have yellow leaves. What's wrong?"
    ]
    
    for question in test_questions:
        print(f"Question: {question}")
        print("-" * 60)
        
        answer = generate_answer(question)
        
        print(f"Answer:\n{answer}")
        print("\n" + "="*60 + "\n")
    
    # Interactive mode
    print("\nInteractive Mode (type 'exit' to quit)")
    print("-" * 60)
    
    while True:
        try:
            user_query = input("\nYour question: ").strip()
            
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            if not user_query:
                continue
            
            print("\nSearching knowledge base...")
            answer = generate_answer(user_query)
            
            print(f"\nAnswer:\n{answer}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
