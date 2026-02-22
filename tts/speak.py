import pyttsx3


class TextToSpeech:
    def __init__(self):
        self.rate = 175
        self.voice_id = None

        # Initialize once to get preferred voice
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'english' in voice.name.lower():
                self.voice_id = voice.id
                break
        engine.stop()
        del engine

        print("TTS initialized")

    def speak(self, text):
        """Speak the text - creates fresh engine each time"""
        print(f"JANET: {text}")

        engine = pyttsx3.init()

        if self.voice_id:
            engine.setProperty('voice', self.voice_id)
        engine.setProperty('rate', self.rate)

        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine