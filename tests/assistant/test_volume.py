# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume tests."""

from unittest.mock import patch

from assistant.volume import STEP, volume


def test_wrong_keyword() -> None:
    """Test wrong Keyword handling."""
    assert volume('Wie viel Uhr ist es') == \
        'Leider kann ich mit diesen Befehl nichts anfangen'


@patch('assistant.volume.os_name', 'nt')
def test_win_up() -> None:
    """Test Volume up for Windows."""
    assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht'


@patch('assistant.volume.os_name', 'nt')
def test_win_down() -> None:
    """Test Volume down for Windows."""
    assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert'


@patch('assistant.volume.os_name', 'nt')
def test_win_mute() -> None:
    """Test Volume mute for Windows."""
    assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt'


@patch('assistant.volume.os_name', 'posix')
def test_lin_up() -> None:
    """Test Volume up for Linux."""
    assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht'


@patch('assistant.volume.os_name', 'posix')
def test_lin_down() -> None:
    """Test Volume down for Linux."""
    assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert'


@patch('assistant.volume.os_name', 'posix')
def test_lin_mute() -> None:
    """Test Volume mute for Linux."""
    assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt'
