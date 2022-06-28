# Copyright 2022  Projektpraktikum Python.
# SPDX-License-Identifier: Apache-2.0
"""Test STT, audio to text."""

from assistant.audio_to_text import audio_to_text

AUDIO_FILE_PATH = './audio_test/classroom-german.wav'
MODEL_FILE_PATH = './src/models/model.tflite'
DESIRED_STR_OUTPUT = 'im klassenzimmer die tarfel der lehrer die lehrerin der tisch der \
stuhl das buch das heft das mepchen der komputer'


def test_wrong_keyword() -> None:
    """Test stt library."""
    assert audio_to_text(MODEL_FILE_PATH, AUDIO_FILE_PATH) == DESIRED_STR_OUTPUT
