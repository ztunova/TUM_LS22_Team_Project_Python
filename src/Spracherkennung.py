import numpy as np
import pyaudio
import time
import wave

from stt import Model

MODEL_PATH = 'model.tflite'
RECORDING_PATH = 'Spracheingabe.wav'


def create_audio(seconds: int) -> str:
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
    lang_model = Model(MODEL_PATH)
    fin = wave.open(RECORDING_PATH, 'rb')
    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
    return str(lang_model.stt(audio))


create_audio(5)
time.sleep(2)
print(convert())
