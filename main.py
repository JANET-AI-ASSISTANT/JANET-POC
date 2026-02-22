import sys
from audio.speech_capture import SpeechCapture
from stt.transcribe import SpeechToText
from intent.scorer import IntentScorer
from response.generator import ResponseGenerator
from tts.speak import TextToSpeech
import config


class JanetPOC:
    def __init__(self):
        print("\n" + "=" * 70)
        print("JANET POC - Initializing...")
        print("=" * 70 + "\n")

        # Initialize all components
        print("1/5 Loading speech capture...")
        self.speech_capture = SpeechCapture()

        print("2/5 Loading speech-to-text (this may take a minute)...")
        self.stt = SpeechToText(model_size='tiny')  # Change to 'base' for better accuracy

        print("3/5 Loading intent scorer...")
        self.intent_scorer = IntentScorer(threshold=config.INTENT_THRESHOLD)

        print("4/5 Loading response generator...")
        self.response_gen = ResponseGenerator()

        print("5/5 Loading text-to-speech...")
        self.tts = TextToSpeech()

        print("\n" + "=" * 70)
        print("JANET POC Ready!")
        print("=" * 70)
        print("\nTry saying:")
        print("  - What time is it?")
        print("  - What's the weather?")
        print("  - Set a timer for 5 minutes")
        print("  - What is 10 plus 5?")
        print("\n(Press Ctrl+C to quit)")
        print("=" * 70 + "\n")

    def run(self):
        """Main loop"""
        self.speech_capture.start()

        try:
            while True:
                # Listen for speech
                print("\n[Listening...]")
                audio = self.speech_capture.listen_for_speech()

                # Transcribe
                print("[Transcribing...]")
                transcript = self.stt.transcribe(audio)
                print(f"Heard: '{transcript}'")

                # Score intent
                score, should_respond, details = self.intent_scorer.score_utterance(transcript)
                print(f"Intent score: {score}")

                if should_respond:
                    print("[Generating response...]")
                    # Generate response
                    response = self.response_gen.generate_response(transcript)

                    # Speak response
                    self.tts.speak(response)
                else:
                    print("(Not addressed to JANET - ignoring)")

        except KeyboardInterrupt:
            print("\n\nStopping JANET...")

        finally:
            self.speech_capture.stop()
            print("JANET stopped. Goodbye!")


def main():
    janet = JanetPOC()
    janet.run()


if __name__ == "__main__":
    main()