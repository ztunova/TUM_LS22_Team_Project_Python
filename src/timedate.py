# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Date and Time Function."""

import datetime


def timedate(taskinput: str) -> str:
    """Use Keywords to find the right function to call.

    Args:
        taskinput: Input from keyword_find as a string

    Returns:
        Current Time or Date.

    """
    time_list = ['Uhrzeit', 'Uhr', 'spaet']
    date_list = ['Datum', 'Tag']
    keylist = [time_list, date_list]

    function_number = 0
    for liste in keylist:
        for element in liste:
            if element in taskinput:
                function_number = keylist.index(liste) + 1

    if function_number == 1:
        return time()

    if function_number == 2:
        return date()

    else:
        return'Leider kann ich mit diesen Befehl nichts anfangen'


def time() -> str:
    """Time function."""
    return f'Es ist {datetime.datetime.now().strftime("%H:%M")}'


def date() -> str:
    """Date function."""
    return f'Es ist der {datetime.datetime.now().strftime("%d/%m/%Y")}'
