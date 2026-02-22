# test_transcribe.py
import sys

sys.path.append('..')

from audio.speech_capture import SpeechCapture
from transcribe import SpeechToText


def test_stt():
    # Initialize
    sc = SpeechCapture()
    stt = SpeechToText(model_size='tiny')  # Use 'base' for better accuracy

    sc.start()

    print("\n" + "=" * 50)
    print("Say something like:")
    print("  - What is the weather today?")
    print("  - What time is it?")
    print("  - Set a timer for 5 minutes")
    print("=" * 50 + "\n")

    # Capture and transcribe 3 utterances
    for i in range(3):
        print(f"\n[{i + 1}/3] Listening...")
        audio = sc.listen_for_speech()

        print("Transcribing...")
        text = stt.transcribe(audio)

        print(f">>> You said: '{text}'")

    sc.stop()


if __name__ == "__main__":
    test_stt()