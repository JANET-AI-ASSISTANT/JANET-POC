from generator import ResponseGenerator


def test_responses():
    print("\n" + "=" * 70)
    print("RESPONSE GENERATION TEST (with Ollama)")
    print("=" * 70)

    print("\nInitializing response generator...")
    gen = ResponseGenerator(use_llm=True)

    if not gen.use_llm:
        print("\nWARNING: Ollama not available, using fallback mode")
        print("Make sure Ollama is running: ollama serve")
        print("And model is downloaded: ollama pull llama3.2:3b\n")

    test_queries = [
        # Direct API calls (not LLM)
        "What time is it?",
        "What's the weather?",
        "Set a timer for 5 minutes",

        # LLM queries
        "What is 10 plus 5?",
        "Tell me a joke",
        "How are you?",
        "What's the capital of France?",
        "Why is the sky blue?",
        "Hello Janet",
    ]

    for query in test_queries:
        print(f"\nQ: {query}")
        response = gen.generate_response(query)
        print(f"A: {response}")
        print("-" * 70)


if __name__ == "__main__":
    test_responses()