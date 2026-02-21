"""
RAG Pipeline: Retrieval-Augmented Generation
Combines FAISS retrieval with LLM for answer generation
"""

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from query import search
import torch

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load LLM for answer generation
# Using a smaller, faster model for demo (can upgrade to Mistral/LLaMA)
print("\nLoading LLM model...")
try:
    # Try to load a small causal LM
    model_name = "distilgpt2"  # Small and fast
    print(f"Loading {model_name}...")
    
    generator = pipeline(
        "text-generation",
        model=model_name,
        tokenizer=model_name,
        device=0 if device == "cuda" else -1,
        max_length=200,
        do_sample=True,
        temperature=0.7,
        pad_token_id=50256
    )
    print("✅ LLM loaded successfully")
except Exception as e:
    print(f"⚠️  Error loading LLM: {e}")
    print("   Using template-based generation instead")
    generator = None


def generate_answer(query: str, use_llm: bool = True) -> str:
    """
    Generate answer using RAG pipeline
    
    Args:
        query: User's question
        use_llm: Whether to use LLM or template-based generation
        
    Returns:
        Generated answer
    """
    # Step 1: Retrieve relevant context
    results = search(query, top_k=3)
    
    if not results:
        return "I couldn't find relevant information. Please consult your local agricultural extension officer."
    
    # Extract context from top results
    context = "\n".join([f"- {r['document']}" for r in results[:3]])
    
    # Step 2: Generate answer
    if use_llm and generator:
        try:
            prompt = f"""You are KrishiSahay, an agricultural expert assistant for Indian farmers.

Farmer Question: {query}

Relevant Agricultural Knowledge:
{context}

Give a concise, practical answer in simple language:"""
            
            response = generator(
                prompt,
                max_length=250,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.2
            )
            
            generated_text = response[0]['generated_text']
            # Extract only the answer part (after the prompt)
            answer = generated_text[len(prompt):].strip()
            
            # Clean up the answer
            if answer:
                # Remove incomplete sentences at the end
                sentences = answer.split('.')
                if len(sentences) > 1:
                    answer = '. '.join(sentences[:-1]) + '.'
                return answer
        except Exception as e:
            print(f"⚠️  LLM generation error: {e}, using template")
    
    # Fallback: Template-based generation
    return generate_template_answer(query, results)


def generate_template_answer(query: str, results: list) -> str:
    """Generate answer using template when LLM is unavailable"""
    if not results:
        return "I couldn't find relevant information. Please consult your local agricultural extension officer."
    
    # Use the most relevant result
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
    print("🤖 RAG Pipeline - Agricultural Q&A")
    print("="*60 + "\n")
    
    # Test questions
    test_questions = [
        "My paddy crop has brown spots. What should I do?",
        "How can I control pests in my cotton field?",
        "When should I apply urea fertilizer?",
        "My plants have yellow leaves. What's wrong?"
    ]
    
    for question in test_questions:
        print(f"❓ Question: {question}")
        print("-" * 60)
        
        answer = generate_answer(question, use_llm=True)
        
        print(f"💡 Answer:\n{answer}")
        print("\n" + "="*60 + "\n")
    
    # Interactive mode
    print("\n🎯 Interactive Mode (type 'exit' to quit)")
    print("-" * 60)
    
    while True:
        try:
            user_query = input("\n👤 Your question: ").strip()
            
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_query:
                continue
            
            print("\n🔍 Searching knowledge base...")
            answer = generate_answer(user_query, use_llm=True)
            
            print(f"\n💡 Answer:\n{answer}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
