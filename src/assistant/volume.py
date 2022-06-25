# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume Function."""

import os

import pyautogui

STEP = 10
OS = os.name


def volume(taskinput: str) -> str:
    """Use Keywords to find the right function to call.

    Args:
        taskinput: Input from keyword_find as a string

    Returns:
        Executed command or error.

    """
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
        pyautogui.press('volumeup', presses=(STEP / 2))

    if OS == 'posix':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ +{STEP}%')


def quieter() -> str:
    """Decrease Volume."""
    if OS == 'nt':
        pyautogui.press('volumedown', presses=(STEP / 2))

    if OS == 'posix':
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ -{STEP}%')


def mute() -> str:
    """Mute Volume."""
    if OS == 'nt':
        pyautogui.press('volumemute')

    if OS == 'posix':
        os.system('pactl set-sink-mute @DEFAULT_SINK@ toggle')
