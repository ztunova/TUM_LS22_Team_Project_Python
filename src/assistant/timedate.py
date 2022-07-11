# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Date and Time Function."""

import datetime
import difflib


def timedate(taskinput: str) -> str:
    """Use Keywords to find the right function to call.

    Args:
        taskinput: Input from keyword_find as a string

    Returns:
        Current Time or Date.

    """
    keyword_to_function = {
        ('uhrzeit', 'uhr', 'spaet'): time,
        ('datum', 'tag'): date,
    }

    word_by_word = taskinput.split()

    for keywords_list, function in keyword_to_function.items():
        for keyword in keywords_list:
            if difflib.get_close_matches(keyword, word_by_word, 1, 0.7) != []:
                return function()

    return 'Leider kann ich mit diesem Befehl nichts anfangen'


def time() -> str:
    """Time function."""
    return f'Es ist {datetime.datetime.now().strftime("%H:%M")}'


def date() -> str:
    """Date function."""
    return f'Es ist der {datetime.datetime.now().strftime("%d/%m/%Y")}'
