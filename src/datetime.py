# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Date and Time Function."""

import datetime


def timedate(taskinput: str) -> str:
    """Use Keywords to find the right function to call.

    Args:
        taskinput: Input from keyword_find as a string

    """
    time_list = ['Uhrzeit', 'Uhr', 'spaet']
    date_list = ['Datum', 'Tag']
