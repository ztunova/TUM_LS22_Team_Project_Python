"""Tests for sprachausgabe.py."""

from assistant.sprachausgabe import speak


def test_tts() -> None:
    """Play a test Strings. Does not actually test correctness."""
    speak('Dies ist ein Test für die Sprachausgabe.')


if __name__ == '__main__':
    test_tts()
