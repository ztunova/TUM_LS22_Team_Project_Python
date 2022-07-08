"""Output spoken text from String."""
import pyttsx3


class TtsEngine():
    """Represent the engine for speech output."""

    def __init__(self) -> None:
        """Initialize the engine and set properties."""
        self.engine = pyttsx3.init()

        self.change_playback_speed(190)

    def change_voice(self, voice_nr: int) -> None:
        """Change the voice of the assistant.

        Args:
            voice_nr: Number of the voice to switch to.

        """
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_nr].id)

    def change_playback_speed(self, speed: int) -> None:
        """Change the playback speed of the assistant.

        Args:
            speed: new playback speed

        """
        self.engine.setProperty('rate', speed)

    def speak(self, output: str) -> None:
        """Convert input text to speech and play it.

        Args:
            output: String of text to be converted.

        """
        self.engine.say(output)
        self.engine.runAndWait()


if __name__ == '__main__':
    tts_engine = TtsEngine()
    tts_engine.speak('Am 28.03.2022 war die Regenwahrscheinlichkeit 15%')
