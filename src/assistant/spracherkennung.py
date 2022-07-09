"""Create audio file from microphone input and convert it to the text."""

import difflib
import wave

import numpy as np
import pyaudio
from stt import Model

from assistant.keyword_find import keyword_find
from assistant.sprachausgabe import TtsEngine

MODEL_PATH = 'src/models/model.tflite'
RECORDING_PATH = 'Spracheingabe.wav'


def create_audio(seconds: int) -> str:
    """Create audio file from microphone input.

    Args:
        seconds: int Duration of the recording

    Returns:
        str: Name of the created recording

    """
    chunk = 1024
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    record_seconds = seconds
    file_name = 'Spracheingabe.wav'

    p_audio = pyaudio.PyAudio()

    stream = p_audio.open(
        format=audio_format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
    )

    print('Aufnahme gestartet')

    frames = []

    for _i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print('Aufnahme beendet')

    stream.stop_stream()
    stream.close()
    p_audio.terminate()

    wave_file = wave.open(file_name, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(p_audio.get_sample_size(audio_format))
    wave_file.setframerate(rate)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

    return file_name


def convert() -> str:
    """Convert audio file to text transcript.

    Returns:
        str: Text transcript of the given audio file

    """
    language_model = Model(MODEL_PATH)
    fin = wave.open(RECORDING_PATH, 'rb')
    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
    return str(language_model.stt(audio))  # model.stt returns Any


def activate_assistant() -> None:
    """Activate assistant on recognized keyword."""
    tts_engine = TtsEngine()
    activated = 0
    no_input = 0
    attempts = 3
    while True:
        create_audio(5)
        text = convert()
        word_by_word = text.split()
        print(text)
        if text != '':
            if no_input != 0:
                no_input = 0
            if difflib.get_close_matches('ausschalten', word_by_word, 1, 0.7) != []:
                tts_engine.speak('assistant turned off')
                break
            if activated:
                result = keyword_find(text, 1, 1)
                tts_engine.speak(result)
        else:
            if no_input == 3:
                tts_engine.speak('assistant turned off')
                break
            no_input = no_input + 1
            print('remaining attempts: ', attempts - no_input)
        # check for keyword for activation
        if difflib.get_close_matches('jarvis', word_by_word, 1, 0.7) != []:
            tts_engine.speak('assistant activated')
            activated = 1


activate_assistant()
