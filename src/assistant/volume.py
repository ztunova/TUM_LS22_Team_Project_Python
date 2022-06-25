# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume Function."""

import os
from os import name as os_name

import pyautogui  # type: ignore

STEP = 10
OS = os_name


def volume(taskinput: str) -> str:
    """Use Keywords to find the right function to call.

    Args:
        taskinput: Input from keyword_find as a string

    Returns:
        Executed command or error.

    """
    taskinput = taskinput.lower()
    up_list = ['lauter']
    down_list = ['leiser']
    mute_list = ['stumm', 'null']
    keylist = [up_list, down_list, mute_list]

    function_number = 0
    for liste in keylist:
        for element in liste:
            if element in taskinput:
                function_number = keylist.index(liste) + 1

    if function_number == 1:
        return louder()

    if function_number == 2:
        return quieter()

    if function_number == 3:
        return mute()

    return 'Leider kann ich mit diesen Befehl nichts anfangen'


def louder() -> str:
    """Increase Volume."""
    if OS == 'nt':
        pyautogui.press('volumeup', presses=int((STEP / 2)))
        return f'Lautstärke wurde um {STEP}% erhöht'

    if OS == 'posix':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ +{STEP}%')
        return f'Lautstärke wurde um {STEP}% erhöht'

    return 'Es ist ein Fehler aufgetreten'


def quieter() -> str:
    """Decrease Volume."""
    if OS == 'nt':
        pyautogui.press('volumedown', presses=int((STEP / 2)))
        return f'Lautstärke wurde um {STEP}% verringert'

    if OS == 'posix':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ -{STEP}%')
        return f'Lautstärke wurde um {STEP}% verringert'

    return 'Es ist ein Fehler aufgetreten'


def mute() -> str:
    """Mute Volume."""
    if OS == 'nt':
        pyautogui.press('volumemute')
        return 'Stummschaltung wurde gedrückt'

    if OS == 'posix':
        os.system('pactl set-sink-mute @DEFAULT_SINK@ toggle')
        return 'Stummschaltung wurde gedrückt'

    return 'Es ist ein Fehler aufgetreten'
