# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Keyword_Finder."""

import difflib

from assistant.timedate import timedate
from assistant.volume import volume


def timer_reminder() -> str:
    """Uebergang.

    Args:
        none

    Returns:
        str: Voiceoutput for user as a string

    Note:
        none

    """
    return 'time-reminder'


def weatherreport() -> str:
    """Uebergang.

    Args:
        none

    Returns:
        str: Voiceoutput for user as a string

    Note:
        none

    """
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
    function_to_number = {
        0: 'Default Fehler',
        1: timedate(voiceinput),
        2: volume(voiceinput),
        3: timer_reminder(),
        4: weatherreport(),
    }

    if qualifier == 2:
        assert function_to_number.get(function_number) is not None, 'Last Function called Fehler'
        return f'{function_to_number.get(function_number)}'

    function_number = 0  # Ohne qualifier == 2 muss die function_number initial auf 0 sein

    timedate_list = ['Uhrzeit', 'Uhr', 'Datum', 'spaet', 'Tag']
    volume_list = ['Lautstaerke', 'leiser', 'lauter']
    timer_list = ['Timer', 'Erinnerung']
    weather_list = ['Wetter', 'Vorhersage']

    # Mapping list for functions
    keylist = [timedate_list, volume_list, timer_list, weather_list]
    word_by_word = voiceinput.split()  # Liste aller Wörter im Befehl

    for liste in keylist:  # Looks if input words mach the keyword list
        for element in liste:
            if difflib.get_close_matches(element, word_by_word, 1, 0.8) != []:
                function_number = keylist.index(liste) + 1  # last call

    assert function_to_number.get(function_number) is not None, 'Function__ to be called Fehler'
    return f'{function_to_number.get(function_number)}'
