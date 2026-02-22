from scorer import IntentScorer


def test_scorer():
    scorer = IntentScorer(threshold=30)

    test_cases = [
        "What is the weather?",
        "What time is it?",
        "Set a timer for 5 minutes",
        "Turn on the lights",
        "I like pizza",
        "Janet, what's the temperature?",
        "Can you check my calendar?",
        "That's really cool",
        "How are you doing?",
        "The weather is nice today",
    ]

    print("\n" + "=" * 70)
    print("INTENT SCORING TEST")
    print("=" * 70)

    for text in test_cases:
        score, should_respond, details = scorer.score_utterance(text)

        status = "RESPOND" if should_respond else "IGNORE"
        print(f"\nText: '{text}'")
        print(f"Score: {score} -> {status}")
        for detail in details:
            print(f"  - {detail}")


if __name__ == "__main__":
    test_scorer()