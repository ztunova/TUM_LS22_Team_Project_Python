"""Create audio file from microphone input and convert it to the text."""

import wave

import numpy as np
import pyaudio  # type: ignore  # module missing library stubs or py.typed marker
from stt import Model  # type: ignore  # module missing library stubs or py.typed marker

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


def find_keyword(transcript: str) -> int:
    """Find if there is a keyword in the speech transcript.

    Args:
        transcript: str Text transcript of the speech

    Returns:
        int: returns 1 if transcript contains keyword, otherwise returns 0

    """
    transcript = transcript.replace(' ', '')
    keywords = ['jerkins', 'jerkyns', 'jelkins', 'jakins', 'jekins']
    for keyword in keywords:
        if keyword in transcript:
            return 1
    return 0


def activate_assistant() -> None:
    """Activate assistant on recognized keyword."""
    activated = 0
    no_input = 0
    attempts = 3
    while True:
        create_audio(5)
        text = convert()
        print(text)
        print(find_keyword(text))
        if activated:
            print('call keyword_find')
        if find_keyword(text):
            activated = 1
        if text == '':
            no_input = no_input + 1
            print('remaining attempts: ', attempts - no_input)
        elif text != '' and no_input > 0:
            no_input = 0
        if no_input == attempts:
            break


activate_assistant()
