# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume tests."""

# import platform
import unittest.mock

from assistant.volume import STEP, volume


def test_wrong_keyword() -> None:
    """Test wrong Keyword handling."""
    assert volume('Wie viel Uhr ist es') == \
        'Leider kann ich mit diesem Befehl nichts anfangen'


@unittest.mock.patch('assistant.volume.os.system')
def test_volume_lin() -> None:
    """Test Volume up, down and mute for all Systems."""
    with unittest.mock.patch('platform.system', return_value='Windows'):
        assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht'
        assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert'
        assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt'

    with unittest.mock.patch('platform.system', return_value='Linux'):
        assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht'
        assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert'
        assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt'

    with unittest.mock.patch('platform.system', return_value='Java'):
        assert volume('Mach lauter') == 'Es ist ein Fehler aufgetreten'
        assert volume('Mach leiser') == 'Es ist ein Fehler aufgetreten'
        assert volume('Mach stumm') == 'Es ist ein Fehler aufgetreten'
