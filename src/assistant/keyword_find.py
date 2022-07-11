# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Keyword_Finder."""

import difflib

from assistant.timedate import timedate
from assistant.volume import volume


def timer_reminder(fake: str) -> str:
    """Uebergang.

    Args:
        fake: str Useless

    Returns:
        str: Voiceoutput for user as a string

    Note:
        none

    """
    fake += fake
    return 'time-reminder'


def weatherreport(fake: str) -> str:
    """Uebergang.

    Args:
        fake: str Useless

    Returns:
        str: Voiceoutput for user as a string

    Note:
        none

    """
    fake += fake
    return 'weatherreport'


def keyword_find(voiceinput: str, qualifier: int, function_number: int) -> str:
    """Use Keywords to find the right function to call.

    Args:
        voiceinput: str Userinput interpreted as a string
        function_number: int
        qualifier: int

    Returns:
        str: Voiceoutput for user as a string

    Note:
        Intern this function excpects the called function to return a
        qualifier, which determins if the function expects
        futher input from the user

    """
    keyword_to_function = {
        ('Uhrzeit', 'Uhr', 'Datum', 'spaet', 'Tag'): timedate,
        ('Lautstaerke', 'leiser', 'lauter'): volume,
        ('Timer', 'Erinnerung'): timer_reminder,
        ('Wetter', 'Vorhersage'): weatherreport,
    }

    if qualifier == 2:
        print(list(keyword_to_function.values()))
        print('das war der output')
        assert len(
            list(keyword_to_function.values()),
        ) >= function_number + 1, 'Invaild last function call'
        return list(keyword_to_function.values())[function_number](voiceinput)

    function_number = 0  # Without qualifiers == 2 fucntion_number has to be 0
    word_by_word = voiceinput.split()  # list of all words in the voiceinput

    for keywords_list, function in keyword_to_function.items():
        for keyword in keywords_list:
            if difflib.get_close_matches(keyword, word_by_word, 1, 0.7):
                return function(voiceinput)

    return 'Leider kann ich mit diesem Befehl nichts anfangen'
