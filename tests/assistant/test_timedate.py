# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Date and Time tests."""

import datetime
from unittest.mock import patch

from assistant.timedate import timedate


# save for later
real_datetime = datetime.datetime

class FakeDatetime:
   """Mock object providing .now interface as datetime does."""
   @staticmethod
   def now() -> datetime.datetime:
       return real_datetime.datetime.fromtimestamp(42)

with patch.object('assistante.timedate.datetime', 'datetime', FakeDatetime):

    def test_time() -> None:
        """Test time function return current time."""
        assert timedate('Wie viel Uhr ist es') == \
            f'Es ist {datetime.datetime.now().strftime("%H:%M")}'


    def test_date() -> None:
        """Test date function return current date."""
        assert timedate('Welcher Tag ist heute') == \
            f'Es ist der {datetime.datetime.now().strftime("%d/%m/%Y")}'


    def test_wrong_keyword() -> None:
        """Test wrong Keyword handling."""
        assert timedate('Wie heißt der Präsident der USA') == \
            'Leider kann ich mit diesen Befehl nichts anfangen'
