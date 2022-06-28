# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Keyword tests."""

import datetime as dt
from unittest.mock import patch

from assistant.keyword_find import keyword_find
from assistant.volume import STEP, volume


def test_keyword_none() -> None:
    """Test Output if function does not exist."""
    assert keyword_find('Blablabla', 1, 1) == 'Default Fehler'


def test_keyword_timedate() -> None:
    """Test Volume down Output."""
    assert keyword_find('Welcher Tag ist heute', 1, 1) == \
        f'Es ist der {dt.datetime.now().strftime("%d/%m/%Y")}'


@patch('assistant.volume.os_name', 'nt')
def test_win_up() -> None:
    """Test Volume up for Windows."""
    assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht'


def test_keyword_timer() -> None:
    """Test Volume down Output."""
    assert keyword_find('Timer fuer 10 Minuten', 1, 1) == 'time-reminder'


def test_keyword_weatherreport() -> None:
    """Test Weatherreport Output."""
    assert keyword_find('Wie wird das Wetter morgen', 1, 1) == 'weatherreport'


def test_keyword_qualifier() -> None:
    """Test Volume down Output."""
    assert keyword_find('Setzte den Timer fuer 10 Minuten', 1, 1) == 'time-reminder'
