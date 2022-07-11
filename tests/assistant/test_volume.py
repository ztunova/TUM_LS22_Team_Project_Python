# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume tests."""

import platform
from unittest.mock import patch

from assistant.volume import STEP, volume


def placeholder_press(inp: str, presses: int = 0) -> str:
    """Replace pyautogui.press."""
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


if platform.system() == 'Windows':

    def test_win_up() -> None:
        """Test Volume up for Windows."""
        with patch('platform.system', return_value='Windows'), \
             patch('assistant.volume.pyautogui.press', placeholder_press):
            assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht win'

    def test_win_down() -> None:
        """Test Volume down for Windows."""
        with patch('platform.system', return_value='Windows'), \
             patch('assistant.volume.pyautogui.press', placeholder_press):
            assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert win'

    def test_win_mute() -> None:
        """Test Volume mute for Windows."""
        with patch('platform.system', return_value='Windows'), \
             patch('assistant.volume.pyautogui.press', placeholder_press):
            assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt win'


def test_lin_up() -> None:
    """Test Volume up for Linux."""
    with patch('platform.system', return_value='Linux'), \
         patch('assistant.volume.os.system', placeholder_press):
        assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht lin'


def test_lin_down() -> None:
    """Test Volume down for Linux."""
    with patch('platform.system', return_value='Linux'), \
         patch('assistant.volume.os.system', placeholder_press):
        assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert lin'


def test_lin_mute() -> None:
    """Test Volume mute for Linux."""
    with patch('platform.system', return_value='Linux'), \
         patch('assistant.volume.os.system', placeholder_press):
        assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt lin'


def test_jav_up() -> None:
    """Test Volume up for unupported OS."""
    with patch('platform.system', return_value='Java'):
        assert volume('Mach lauter') == 'Es ist ein Fehler aufgetreten'


def test_jav_down() -> None:
    """Test Volume up for unupported OS."""
    with patch('platform.system', return_value='Java'):
        assert volume('Mach leiser') == 'Es ist ein Fehler aufgetreten'


def test_jav_mute() -> None:
    """Test Volume up for unupported OS."""
    with patch('platform.system', return_value='Java'):
        assert volume('Mach stumm') == 'Es ist ein Fehler aufgetreten'
