"""Output spoken text from String."""
import pyttsx3


def speak(output: str) -> None:
    """Convert input text to speech and play it.

    Args:
        output: String of text to be converted.

    """
    engine = pyttsx3.init()
    # Change voice to english
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[1].id)
    # Change playback speed
    engine.setProperty('rate', 190)
    # Output text
    engine.say(output)
    engine.runAndWait()


if __name__ == '__main__':
    speak('Am 28.03.2022 war die Regenwahrscheinlichkeit 15%')
