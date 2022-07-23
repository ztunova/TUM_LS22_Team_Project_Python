"""Test for spracherkennung.py."""

import difflib
from unittest.mock import patch

from assistant.spracherkennung import activate_assistant, convert


def placeholder_ausschalten(audio_file: str = 'Spracheingabe.wav') -> str:
    """Fake placholder function for patches."""
    print(audio_file)
    return 'ausschalten'


def placeholder_no_input(audio_file: str = 'Spracheingabe.wav') -> str:
    """Fake placholder function for patches."""
    print(audio_file)
    return ''


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
    with patch('assistant.spracherkennung.convert', placeholder_ausschalten):
        assert activate_assistant(use_predefined_audio=True) == 0


def test_ausschalten_no_input() -> None:
    """Test turn off the assistant after 3-times no input."""
    with patch('assistant.spracherkennung.convert', placeholder_no_input):
        assert activate_assistant(use_predefined_audio=True) == 0


def test_activate_no_keyword() -> None:
    """Test to activate assistant with keyword, but not calling keyword_find."""
    with patch('assistant.spracherkennung.convert', side_effect=['start', '', 'ausschalten']):
        assert activate_assistant(use_predefined_audio=True) == 1


def test_activate_with_keyword() -> None:
    """Test to activate assistant with keyword, with calling keyword_find."""
    with patch('assistant.spracherkennung.convert', side_effect=['start', 'uhr', 'ausschalten']):
        assert activate_assistant(use_predefined_audio=True) == 1
