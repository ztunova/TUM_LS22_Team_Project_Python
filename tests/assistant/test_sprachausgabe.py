"""Tests for sprachausgabe.py."""

from assistant.sprachausgabe import TtsEngine


def test_tts() -> None:
    """Play a test Strings. Does not actually test correctness."""
    engine = TtsEngine()
    engine.speak('Dies ist ein Test für die Sprachausgabe.')


if __name__ == '__main__':
    test_tts()
