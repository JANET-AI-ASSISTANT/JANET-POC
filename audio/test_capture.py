import time
from capture import AudioCapture


def test_capture():
    capture = AudioCapture()
    capture.start()

    print("Capturing audio for 10 seconds...")
    for i in range(20):  # 20 iterations = ~10 seconds
        time.sleep(0.5)
        chunk = capture.get_latest_chunk()
        if chunk is not None:
            # Calculate volume (RMS)
            rms = np.sqrt(np.mean(chunk ** 2))
            print(f"Chunk {i}: RMS volume = {rms:.0f}")

    capture.stop()


if __name__ == "__main__":
    import numpy as np

    test_capture()