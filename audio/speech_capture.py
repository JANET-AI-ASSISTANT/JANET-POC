#speech_capture.py

import time
import numpy as np
from .capture import AudioCapture
from .vad import VoiceActivityDetector


class SpeechCapture:
    def __init__(self):
        self.capture = AudioCapture()
        self.vad = VoiceActivityDetector(threshold=0.5)

        self.is_capturing = False
        self.speech_frames = []
        self.silence_counter = 0
        self.SILENCE_THRESHOLD = 27  # ~800ms at 30ms per frame

    def start(self):
        """Start the audio capture"""
        self.capture.start()

    def stop(self):
        """Stop the audio capture"""
        self.capture.stop()

    def listen_for_speech(self):
        """
        Continuously listen and return complete speech when detected
        Returns: numpy array of speech audio, or None
        """
        while True:
            time.sleep(0.03)  # 30ms
            chunk = self.capture.get_latest_chunk()

            if chunk is None:
                continue

            is_speech = self.vad.check_speech(chunk)

            if not self.is_capturing:
                # IDLE state - waiting for speech
                if is_speech:
                    print("Speech detected, capturing...")
                    self.is_capturing = True
                    self.speech_frames = []
                    # Include some buffer audio
                    buffer_audio = self.capture.get_buffer_audio()
                    if buffer_audio is not None:
                        # Get last 0.5 seconds
                        buffer_samples = int(0.5 * 16000)
                        self.speech_frames.append(buffer_audio[-buffer_samples:])

            else:
                # CAPTURING state
                self.speech_frames.append(chunk)

                if is_speech:
                    # Still speaking
                    self.silence_counter = 0
                else:
                    # Silence detected
                    self.silence_counter += 1

                    if self.silence_counter >= self.SILENCE_THRESHOLD:
                        # End of speech
                        print("Speech ended, processing...")
                        self.is_capturing = False
                        self.silence_counter = 0

                        # Concatenate all frames
                        full_audio = np.concatenate(self.speech_frames)
                        self.speech_frames = []

                        return full_audio