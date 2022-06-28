# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Keyword_Finder."""

# To Do: Echte volume und timedate aufrufe impementieren

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
        return f'{function_to_number.get(function_number)}'

    function_number = 0  # Ohne qualifier == 2 muss die function_number auf 0 sein

    timedate_list = ['Uhrzeit', 'Uhr', 'Datum', 'spaet', 'Tag']
    volume_list = ['Lautstaerke', 'leiser', 'lauter']
    timer_list = ['Timer', 'Erinnerung']
    weather_list = ['Wetter', 'Vorhersage']

    # Mapping list for functions
    keylist = [timedate_list, volume_list, timer_list, weather_list]

    for liste in keylist:  # Looks if input words mach the keyword list
        for element in liste:
            if element in voiceinput:
                function_number = keylist.index(liste) + 1  # last call

    return f'{function_to_number.get(function_number)}'
