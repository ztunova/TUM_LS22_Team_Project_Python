# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Volume tests."""

import platform
from unittest.mock import patch

from assistant.volume import STEP, volume


def test_wrong_keyword() -> None:
    """Test wrong Keyword handling."""
    assert volume('Wie viel Uhr ist es') == \
        'Leider kann ich mit diesem Befehl nichts anfangen'


with patch('assistant.volume.os') as os_mock:
    if platform.system() == 'Windows':
        with patch('assistant.volume.pyautogui') as pyautogui_mock:

            def test_volume_win() -> None:
                """Test Volume up, down and mute for all Systems."""
                pyautogui_mock.return_value = 'Ausgeführt'
                os_mock.return_value = 'Ausgeführt'
                with patch('platform.system', return_value='Windows'):
                    assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht'
                    assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert'
                    assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt'

                with patch('platform.system', return_value='Linux'):
                    assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht'
                    assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert'
                    assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt'

                with patch('platform.system', return_value='Java'):
                    assert volume('Mach lauter') == 'Es ist ein Fehler aufgetreten'
                    assert volume('Mach leiser') == 'Es ist ein Fehler aufgetreten'
                    assert volume('Mach stumm') == 'Es ist ein Fehler aufgetreten'

    def test_volume_lin() -> None:
        """Test Volume up, down and mute for all Systems."""
        os_mock.return_value = 'Ausgeführt'
        with patch('platform.system', return_value='Windows'):
            assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht'
            assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert'
            assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt'

        with patch('platform.system', return_value='Linux'):
            assert volume('Mach lauter') == f'Lautstärke wurde um {STEP}% erhöht'
            assert volume('Mach leiser') == f'Lautstärke wurde um {STEP}% verringert'
            assert volume('Mach stumm') == 'Stummschaltung wurde gedrückt'

        with patch('platform.system', return_value='Java'):
            assert volume('Mach lauter') == 'Es ist ein Fehler aufgetreten'
            assert volume('Mach leiser') == 'Es ist ein Fehler aufgetreten'
            assert volume('Mach stumm') == 'Es ist ein Fehler aufgetreten'
