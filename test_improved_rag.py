from agents_improved import answer_question

print("Testing improved RAG system...")
print("="*50)

# Test questions
questions = [
    "Explain F1 tire compounds",
    "How does DRS work?", 
    "What is ground effect in F1?",
    "Tell me about F1 power units",
    "How do F1 brake systems work?"
]

for question in questions:
    print(f"\nQ: {question}")
    print("-" * 30)
    try:
        answer, sources = answer_question(question)
        print(f"A: {answer[:200]}...")
        print(f"Sources: {len(sources)} found")
        for i, src in enumerate(sources[:2], 1):
            print(f"  {i}. {src[:80]}...")
    except Exception as e:
        print(f"Error: {e}")
    print()

print("="*50)
