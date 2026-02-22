# transcribe.py
import whisper
import numpy as np


class SpeechToText:
    def __init__(self, model_size='tiny'):
        """
        model_size: 'tiny', 'base', 'small'
        tiny = fastest, least accurate
        base = good balance
        small = best quality (but slower)
        """
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        print("Whisper model loaded")

    def transcribe(self, audio_data, sample_rate=16000):
        """
        Transcribe audio to text
        audio_data: numpy array (int16 or float32)
        Returns: transcript text (string)
        """
        # Whisper expects float32 in range [-1, 1]
        if audio_data.dtype == np.int16:
            audio_float = audio_data.astype(np.float32) / 32768.0
        else:
            audio_float = audio_data

        # Transcribe
        result = self.model.transcribe(
            audio_float,
            language='en',  # Can be None for auto-detect
            fp16=False  # Use fp32 for CPU
        )

        transcript = result['text'].strip()
        return transcript