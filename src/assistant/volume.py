# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume Function."""

import difflib
import os
import platform

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
    taskinput = taskinput.lower()

    keyword_to_function = {
        ('stumm', 'null', 'mute'): mute,
        ('lauter', 'erhö'): louder,
        ('leiser', 'senke'): quieter,
    }

    word_by_word = taskinput.split()  # list of all words in the voiceinput

    for keywords_list, function in keyword_to_function.items():
        for keyword in keywords_list:
            if difflib.get_close_matches(keyword, word_by_word, 1, 0.7) != []:
                return function(STEP)

    return 'Leider kann ich mit diesem Befehl nichts anfangen'


def louder(step: int) -> str:
    """Increase Volume."""
    if platform.system() == 'Windows':
        pyautogui.press('volumeup', presses=int((step / 2)))
        # Pyautogui kann die lautsärke nur in 2% Schritten ändern
        return f'Lautstärke wurde um {step}% erhöht'

    if platform.system() == 'Linux':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ +{step}%')
        return f'Lautstärke wurde um {step}% erhöht'

    return 'Leider kann ich mit diesem Befehl nichts anfangen'


def quieter(step: int) -> str:
    """Decrease Volume."""
    if platform.system() == 'Windows':
        pyautogui.press('volumedown', presses=int((step / 2)))
        # Pyautogui kann die lautsärke nur in 2% Schritten ändern
        return f'Lautstärke wurde um {step}% verringert'

    if platform.system() == 'Linux':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ -{step}%')
        return f'Lautstärke wurde um {step}% verringert'

    return 'Leider kann ich mit diesem Befehl nichts anfangen'


def mute(step: int) -> str:
    """Mute Volume."""
    step += step
    if platform.system() == 'Windows':
        pyautogui.press('volumemute', presses=1)
        return 'Stummschaltung wurde gedrückt'

    if platform.system() == 'Linux':
        os.system('pactl set-sink-mute @DEFAULT_SINK@ toggle')
        return 'Stummschaltung wurde gedrückt'

    return 'Leider kann ich mit diesem Befehl nichts anfangen'
