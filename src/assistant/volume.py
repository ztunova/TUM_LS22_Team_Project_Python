# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume Function."""

import difflib
import platform
import os

if platform.system() == 'Windows':
    import pyautogui

STEP = 10


def volume(taskinput: str) -> str:
    """Use Keywords to find the right function to call.

    Args:
        taskinput: Input from keyword_find as a string

    Returns:
        Executed command or error.

    """
    keyword_to_function = {
        ('stumm', 'null', 'mute'): mute(),
        ('lauter', 'erhöhen'): louder(),
        ('leiser', 'verringern'): quieter(),
    }

    word_by_word = taskinput.split()

    for keywords_list, function in keyword_to_function.items():
        for keyword in keywords_list:
            if difflib.get_close_matches(keyword, word_by_word, 1, 0.8) != []:
                return function

    return 'Leider kann ich mit diesem Befehl nichts anfangen'


def louder() -> str:
    """Increase Volume."""
    if platform.system() == 'Windows':
        pyautogui.press('volumeup', presses=int((STEP / 2)))
        # Pyautogui kann die lautsärke nur in 2% Schritten ändern
        return f'Lautstärke wurde um {STEP}% erhöht win'

    if platform.system() == 'Linux':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ +{STEP}%')
        return f'Lautstärke wurde um {STEP}% erhöht lin'

    return 'Es ist ein Fehler aufgetreten'


def quieter() -> str:
    """Decrease Volume."""
    if platform.system() == 'Windows':
        pyautogui.press('volumedown', presses=int((STEP / 2)))
        # Pyautogui kann die lautsärke nur in 2% Schritten ändern
        return f'Lautstärke wurde um {STEP}% verringert win'

    if platform.system() == 'Linux':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ -{STEP}%')
        return f'Lautstärke wurde um {STEP}% verringert lin'

    return 'Es ist ein Fehler aufgetreten'


def mute() -> str:
    """Mute Volume."""
    if platform.system() == 'Windows':
        pyautogui.press('volumemute', presses=1)
        return 'Stummschaltung wurde gedrückt win'

    if platform.system() == 'Linux':
        os.system('pactl set-sink-mute @DEFAULT_SINK@ toggle')
        return 'Stummschaltung wurde gedrückt lin'

    return 'Es ist ein Fehler aufgetreten'
