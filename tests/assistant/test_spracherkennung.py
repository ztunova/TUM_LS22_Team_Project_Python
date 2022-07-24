"""Test for spracherkennung.py."""

import difflib
from unittest.mock import patch

import numpy as np
import pyaudio

from assistant.spracherkennung import activate_assistant, convert, create_audio


class FakeStream:
    """Fake placeholder class to patch stream."""

    def __init__(self, audio_format: pyaudio.paInt16, channels: int, rate: int, chunk: int):
        """Initialize test object."""
        self.format = audio_format
        self.channels = channels
        self.rate = rate
        self.input = True
        self.frames_per_buffer = chunk

    def read(self, chunk: int) -> bytes:
        """Fake placeholder method for stream.read."""
        print(f'reading {self.frames_per_buffer}')
        return np.random.randint(-(2**15), (2**15) - 1, chunk, dtype=np.int16).tobytes()

    def stop_stream(self) -> None:
        """Fake method to patch stream.stop_stream."""
        print(f'stop mock stream {self.rate}')

    def close(self) -> None:
        """Fake method to patch stream.close."""
        print(f'close mock stream {self.rate}')


class PlaceholderPyAudio:
    """Fake placeholder class to patch PyAudio."""

    def __init__(self) -> None:
        """Initialize test object."""
        print('Working!!!!')

    def open(  # pylint: disable=too-many-arguments
        self,  # pylint: disable=redefined-builtin, unused-argument
        format: pyaudio.paInt16,  # pylint: disable=redefined-builtin
        channels: int,
        rate: int,
        input: bool,  # pylint: disable=redefined-builtin, unused-argument
        frames_per_buffer: int,
    ) -> FakeStream:
        """Fake function to patch PyAudio.open."""
        print(f'open mock PyAudio {self.__class__}')
        return FakeStream(format, channels, rate, frames_per_buffer)

    def terminate(self) -> None:
        """Fake method to patch PyAudio.terminate."""
        print(f'terminate mock PyAudio {self.__class__}')

    def get_sample_size(self, audio_format: pyaudio.paInt16) -> int:
        """Fake method to patch PyAudio.get_sample_rate."""
        print(f'get sample size {self.__class__}')
        if audio_format == pyaudio.paInt16:
            return 2
        return 1


def test_create_audio() -> None:
    """Test turn off the assistant after ausschalten keyword."""
    with patch('assistant.spracherkennung.pyaudio.PyAudio', PlaceholderPyAudio):
        assert create_audio(5) == 'Spracheingabe.wav'


def placeholder_ausschalten(audio_file: str = 'Spracheingabe.wav') -> str:
    """Fake placholder function for patches."""
    print(audio_file)
    return 'ausschalten'


def placeholder_no_input(audio_file: str = 'Spracheingabe.wav') -> str:
    """Fake placholder function for patches."""
    print(audio_file)
    return ''


def placeholder_create_audio(fake_sec: int) -> str:
    """Fake placeholder function for patching create audio function."""
    print(fake_sec)
    return 'audio_test/Start.wav'


def test_keyword_recognition() -> None:
    """Test recognition of keywords."""
    text = str(convert('audio_test/Start.wav'))
    word_by_word = text.split()
    assert difflib.get_close_matches('start', word_by_word, 1, 0.7) != []
    text = str(convert('audio_test/Ausschalten.wav'))
    word_by_word = text.split()
    assert difflib.get_close_matches('ausschalten', word_by_word, 1, 0.7) != []


def test_ausschalten_keyword() -> None:
    """Test turn off the assistant after ausschalten keyword."""
    with patch('assistant.spracherkennung.convert', placeholder_ausschalten), \
         patch('assistant.spracherkennung.create_audio', placeholder_create_audio):
        assert activate_assistant() == 0


def test_ausschalten_no_input() -> None:
    """Test turn off the assistant after 3-times no input."""
    with patch('assistant.spracherkennung.convert', placeholder_no_input), \
         patch('assistant.spracherkennung.create_audio', placeholder_create_audio):
        assert activate_assistant() == 0


def test_activate_no_keyword() -> None:
    """Test to activate assistant with keyword, but not calling keyword_find."""
    with patch('assistant.spracherkennung.convert', side_effect=['start', '', 'ausschalten']), \
         patch('assistant.spracherkennung.create_audio', placeholder_create_audio):
        assert activate_assistant() == 1


def test_activate_with_keyword() -> None:
    """Test to activate assistant with keyword, with calling keyword_find."""
    with patch('assistant.spracherkennung.convert', side_effect=['start', 'uhr', 'ausschalten']), \
         patch('assistant.spracherkennung.create_audio', placeholder_create_audio):
        assert activate_assistant() == 1
