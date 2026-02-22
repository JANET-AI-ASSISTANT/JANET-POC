import time
import numpy as np
from capture import AudioCapture
from vad import VoiceActivityDetector


def test_vad():
    capture = AudioCapture()
    vad = VoiceActivityDetector(threshold=0.5)

    capture.start()
    print("Speak to test VAD... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(0.03)  # 30ms
            chunk = capture.get_latest_chunk()

            if chunk is not None:
                prob = vad.is_speech(chunk)
                is_speech = prob >= 0.5

                status = "SPEECH" if is_speech else "silence"
                print(f"{status:8s} - probability: {prob:.2f}")

    except KeyboardInterrupt:
        print("\nStopping...")

    capture.stop()


if __name__ == "__main__":
    test_vad()