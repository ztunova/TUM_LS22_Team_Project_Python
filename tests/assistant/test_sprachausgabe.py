"""Tests for sprachausgabe.py."""

from unittest.mock import MagicMock, patch

from assistant.sprachausgabe import TtsEngine


class WrongArgumentError(Exception):
    """Signal that a function was called with a wrong argument."""


class DummyVoice():
    """Dummy class mimicing the voice object in pyttsx3."""

    # Disable pylint errors: class has to mimic voice object
    # pylint: disable=too-few-public-methods,invalid-name
    def __init__(self, number: int) -> None:
        """Init function.

        Args:
            number: the id of the voice

        """
        self.id = number


class TestEngine():
    """Test class for the custom class TtsEngine."""

    def __init__(self) -> None:
        """Initialize test object."""
        self.mocked = MagicMock()
        self.engine = self.test_init()

    def test_init(self) -> TtsEngine:
        """Test the init function."""
        with patch('pyttsx3.init', side_effect=self.mocked):
            return TtsEngine()

    def test_change_voice(self) -> None:
        """Test the change voice function."""
        self.mocked.return_value.getProperty.return_value = \
            [DummyVoice(0), DummyVoice(1), DummyVoice(2), DummyVoice(3)]
        self.engine.change_voice(2)
        self.mocked.return_value.getProperty.assert_called_with('voices')
        self.mocked.return_value.setProperty.assert_called_with('voice', 2)

    def test_change_playback_speed(self) -> None:
        """Test the change playback speed function."""
        self.engine.change_playback_speed(150)
        self.mocked.return_value.setProperty.assert_called_with('rate', 150)

    def test_speak(self) -> None:
        """Test the speak function."""
        self.engine.speak('Dies ist ein Test.')
        self.mocked.return_value.say.assert_called_with('Dies ist ein Test.')
        self.mocked.return_value.runAndWait.assert_called()


def test_run() -> None:
    """Runs all Test from the TestEngine class."""
    test = TestEngine()
    test.test_change_playback_speed()
    test.test_change_voice()
    test.test_speak()


if __name__ == '__main__':
    test_run()
