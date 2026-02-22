# vad.py
import torch
import numpy as np


class VoiceActivityDetector:
    def __init__(self, threshold=0.5):
        # Load Silero VAD model
        model, utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=False
        )

        self.model = model
        self.threshold = threshold
        self.get_speech_timestamps = utils[0]

        print("VAD model loaded")

    def is_speech(self, audio_chunk, sample_rate=16000):
        """
        Check if audio chunk contains speech
        audio_chunk: numpy array of int16
        Returns: float probability (0-1)
        """
        # Convert to float32 and normalize to [-1, 1]
        audio_float = audio_chunk.astype(np.float32) / 32768.0

        # Convert to torch tensor
        audio_tensor = torch.from_numpy(audio_float)

        # Get speech probability
        speech_prob = self.model(audio_tensor, sample_rate).item()

        return speech_prob

    def check_speech(self, audio_chunk, sample_rate=16000):
        """Returns True if speech detected above threshold"""
        prob = self.is_speech(audio_chunk, sample_rate)
        return prob >= self.threshold