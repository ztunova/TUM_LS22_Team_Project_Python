# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume Function."""

# import difflib
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

    if 'stumm' in taskinput:
        return mute()

    if 'null' in taskinput:
        return mute()

    if 'leiser' in taskinput:
        return quieter()

    if 'lauter' in taskinput:
        return louder()

    return 'Leider kann ich mit diesem Befehl nichts anfangen'


def louder() -> str:
    """Increase Volume."""
    if platform.system() == 'Windows':
        pyautogui.press('volumeup', presses=int((STEP / 2)))
        # Pyautogui kann die lautsärke nur in 2% Schritten ändern
        return f'Lautstärke wurde um {STEP}% erhöht'

    if platform.system() == 'Linux':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ +{STEP}%')
        return f'Lautstärke wurde um {STEP}% erhöht'

    return 'Es ist ein Fehler aufgetreten'


def quieter() -> str:
    """Decrease Volume."""
    if platform.system() == 'Windows':
        pyautogui.press('volumedown', presses=int((STEP / 2)))
        # Pyautogui kann die lautsärke nur in 2% Schritten ändern
        return f'Lautstärke wurde um {STEP}% verringert'

    if platform.system() == 'Linux':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ -{STEP}%')
        return f'Lautstärke wurde um {STEP}% verringert'

    return 'Es ist ein Fehler aufgetreten'


def mute() -> str:
    """Mute Volume."""
    if platform.system() == 'Windows':
        pyautogui.press('volumemute', presses=1)
        return 'Stummschaltung wurde gedrückt'

    if platform.system() == 'Linux':
        os.system('pactl set-sink-mute @DEFAULT_SINK@ toggle')
        return 'Stummschaltung wurde gedrückt'

    return 'Es ist ein Fehler aufgetreten'
