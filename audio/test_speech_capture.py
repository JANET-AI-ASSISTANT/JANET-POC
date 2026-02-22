# test_speech_capture
from speech_capture import SpeechCapture
import numpy as np
import wave


def test_speech_capture():
    sc = SpeechCapture()
    sc.start()

    print("Say something... waiting for speech...")

    # Capture one utterance
    audio = sc.listen_for_speech()

    print(f"Captured {len(audio)} samples ({len(audio) / 16000:.2f} seconds)")

    # Save to file
    with wave.open("captured_speech.wav", 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio.tobytes())

    print("Saved to captured_speech.wav")

    sc.stop()


if __name__ == "__main__":
    test_speech_capture()