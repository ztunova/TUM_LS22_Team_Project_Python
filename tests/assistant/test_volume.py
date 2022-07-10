# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume tests."""

# import platform
from unittest.mock import patch

from assistant.volume import STEP, volume


def mock_win(inp: str, presses: int) -> str:
    """Windows Mock."""
    print(inp)
    print(presses)
    return inp


def mock_lin(inp: str) -> str:
    """Linux Mock."""
    print(inp)
    return inp


def test_wrong_keyword() -> None:
    """Test wrong Keyword handling."""
    assert volume('Wie viel Uhr ist es') == \
        'Leider kann ich mit diesem Befehl nichts anfangen'


def test_volume() -> None:
    """Test Volume up, down and mute for all Systems."""
    with patch('platform.system', return_value='Windows'),\
         patch('assistant.volume.pyautogui.press', mock_win):
        assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht win'
        assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert win'
        assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt win'

    with patch('platform.system', return_value='Linux'),\
         patch('assistant.volume.os.system', mock_lin):
        assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht lin'
        assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert lin'
        assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt lin'

    with patch('platform.system', return_value='Java'):
        assert volume('Mach lauter') == 'Es ist ein Fehler aufgetreten'
        assert volume('Mach leiser') == 'Es ist ein Fehler aufgetreten'
        assert volume('Mach stumm') == 'Es ist ein Fehler aufgetreten'
