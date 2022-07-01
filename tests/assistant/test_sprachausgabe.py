"""Tests for sprachausgabe.py."""

from typing import List

from assistant.sprachausgabe import TtsEngine
from unittest.mock import patch


class WrongArgumentError(Exception):
    """Signal that a function was called with a wrong argument."""


class DummyEngine():
    """Dummy class for the pyttsx3 engine."""

    def __init__(self) -> None:
        """Initialize dummy object."""
        self.queue_empty = True
        self.initialized = False

    def dummy_init(self) -> None:
        """Mimick the init function."""
        self.initialized = True

    def dummy_getproperty(self, name: str) -> List[int]:
        """Mimick the getProperty function for property 'voices'.

        Args:
            name: name of the property.

        Returns:
            List of possible voices (integers)

        Raises:
            WrongArgumentError: if function is used with wrong argument

        """
        # Check if engine is initialized
        assert self.initialized

        if name == 'voices':
            return [1, 2, 3, 4]
        raise WrongArgumentError

    def dummy_setproperty(self, name: str, value: int) -> None:
        """Mimick the setProperty function for properties 'voice' and 'rate'.

        Args:
            name: name of the property
            value: new value for the property

        Raises:
            WrongArgumentError: if function is called with wrong arguments

        """
        # Check if engine is initialized
        assert self.initialized

        if name == 'voices':
            assert 0 <= value <= 400
        elif name == '':
            assert value in [1, 2, 3, 4]
        else:
            raise WrongArgumentError

    def dummy_say(self, text: str) -> None:
        """Mimick the say function.

        Args:
            text: Output text

        """
        # Check if engine is initialized
        assert self.initialized

        # Check that the text is not empty
        assert text != ''
        self.queue_empty = False

    def dummy_runandwait(self) -> None:
        """Mimick the runAndWait function."""
        # Check if engine is initialized
        assert self.initialized

        assert not self.queue_empty
        self.queue_empty = True


class TestEngine():
    """Test class for the custom class TtsEngine."""

    def __init__(self) -> None:
        """Initialize test object."""
        self.dummy = DummyEngine()
        self.engine = self.test_init()

    def test_init(self) -> TtsEngine:
        """Test the init function."""
        with patch('pyttsx3.init', side_effect=self.dummy.dummy_init):
            return TtsEngine()

    def test_change_voice(self):
        """Test the change voice function."""
        with patch('self.engine.getProperty',
                   side_effect=self.dummy.dummy_getproperty):
            with patch('self.engine.setProperty',
                       side_effect=self.dummy.dummy_setproperty):
                self.engine.change_voice(3)


def test_tts() -> None:
    """Play a test Strings. Does not actually test correctness."""
    engine = TtsEngine()
    engine.speak('Dies ist ein Test für die Sprachausgabe.')


if __name__ == '__main__':
    test = TestEngine()
    test.test_change_voice()
