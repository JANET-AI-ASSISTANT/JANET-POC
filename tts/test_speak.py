#test_speak.py
from speak import TextToSpeech


def test_tts():
    tts = TextToSpeech()

    test_phrases = [
        "Hello, I am Janet.",
        "The time is 3:45 PM",
        "The weather is sunny with a temperature of 25 degrees",
        "Timer set for 5 minutes"
    ]

    print("\n" + "=" * 70)
    print("TEXT-TO-SPEECH TEST")
    print("=" * 70)

    for phrase in test_phrases:
        print(f"\nSpeaking: {phrase}")
        tts.speak(phrase)


if __name__ == "__main__":
    test_tts()