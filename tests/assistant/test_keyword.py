# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Keyword tests."""

import datetime as dt
from unittest.mock import patch

from assistant.keyword_find import keyword_find
from assistant.volume import STEP

# Fake function for patches


def placeholder(fake: str) -> str:
    """Fake placholder function for patches."""
    return fake


def placeholder_press(inp: str, presses: int = 0) -> str:
    """Replace pyautogui.press."""
    print(inp)
    print(presses)
    return inp


# Test for right mapping from keyword_find


def test_keyword_none() -> None:
    """Test Output if function does not exist."""
    assert keyword_find('Blablabla', 1, 0) == 'Leider kann ich mit diesem Befehl nichts anfangen'


def test_keyword_timedate() -> None:
    """Test Timedate Call."""
    with patch('assistant.keyword_find.timedate', placeholder):
        assert keyword_find('ur', 1, 0) == 'ur'


def test_keyword_volume() -> None:
    """Test Volume Call."""
    with patch('assistant.keyword_find.volume', placeholder):
        assert keyword_find('Mach lauter', 1, 0) == 'Mach lauter'


def test_keyword_timer() -> None:
    """Test Timer Call."""
    assert keyword_find('timer fuer 10 minuten', 1, 0) == 'time-reminder'


def test_keyword_weatherreport() -> None:
    """Test Weatherreport Call."""
    assert keyword_find('wie wird das wetter morgen', 1, 0) == 'weatherreport'


# Test actuall function call to be correct (copy paste test from Plug-In functions)


def test_full_call_keyword_volume() -> None:
    """Test Volume up for Linux."""
    with patch('platform.system', return_value='Linux'), \
         patch('assistant.volume.os.system', placeholder_press):
        assert keyword_find('Mach lauter', 1, 0) == f'Lautstärke wurde um {STEP}% erhöht'


def test_full_call_keyword_timedate() -> None:
    """Test Date Output."""
    assert keyword_find('welcher tag ist heute', 1, 0) == \
        f'Es ist der {dt.datetime.now().strftime("%d/%m/%Y")}'


# Test all cases, where a function is recalled (qualifierer == 2)


def test_keyword_qualifiers() -> None:
    """Test if last function called is executed correctly."""
    assert keyword_find('welcher tag ist heute', 2, 0) == \
        f'Es ist der {dt.datetime.now().strftime("%d/%m/%Y")}'
    with patch('platform.system', return_value='Linux'), \
         patch('assistant.volume.os.system', placeholder_press):
        assert keyword_find('Mach lauter', 2, 1) == f'Lautstärke wurde um {STEP}% erhöht'
    assert keyword_find('setzte den timer fuer 10 Minuten', 2, 2) == 'time-reminder'
    assert keyword_find('wie wird das wetter morgen', 2, 3) == 'weatherreport'
    # assert keyword_find('Unbekannte Funktion', 2, 4) == 'Invaild last function call'


# Test for words with an error in them


def test_keyword_with_errors() -> None:
    """Test if keywords with spellimng mistakes are sitll recognised."""
    with patch('assistant.keyword_find.timedate', placeholder):
        assert keyword_find('ur', 1, 0) == 'ur'
        assert keyword_find('urzet', 1, 0) == 'urzet'
        assert keyword_find('datu', 1, 0) == 'datu'
        assert keyword_find('spet', 1, 0) == 'spet'

    with patch('assistant.keyword_find.volume', placeholder):
        assert keyword_find('later', 1, 0) == 'later'
        assert keyword_find('laiser', 1, 0) == 'laiser'
