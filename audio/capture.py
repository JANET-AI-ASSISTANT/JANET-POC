# capture.py

import pyaudio
import numpy as np
from collections import deque


class AudioCapture:
    def __init__(self, rate=16000, chunk=512, buffer_seconds=5):
        self.RATE = rate
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

        # Rolling buffer (5 seconds)
        buffer_size = int(rate * buffer_seconds / chunk)
        self.buffer = deque(maxlen=buffer_size)

        self.p = pyaudio.PyAudio()
        self.stream = None

    def start(self):
        """Start capturing audio"""
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self._callback
        )
        self.stream.start_stream()
        print("Audio capture started")

    def _callback(self, in_data, frame_count, time_info, status):
        """Called by PyAudio for each audio chunk"""
        self.buffer.append(in_data)
        return (in_data, pyaudio.paContinue)

    def get_latest_chunk(self):
        """Get the most recent audio chunk as numpy array"""
        if len(self.buffer) == 0:
            return None

        # Convert bytes to numpy array
        audio_data = np.frombuffer(self.buffer[-1], dtype=np.int16)
        return audio_data

    def get_buffer_audio(self):
        """Get all buffered audio as numpy array"""
        if len(self.buffer) == 0:
            return None

        # Concatenate all chunks
        audio_bytes = b''.join(self.buffer)
        audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
        return audio_data

    def clear_buffer(self):
        """Clear the rolling buffer"""
        self.buffer.clear()

    def stop(self):
        """Stop capturing"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        print("Audio capture stopped")