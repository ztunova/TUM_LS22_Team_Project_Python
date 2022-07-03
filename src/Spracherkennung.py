import pyaudio
import wave
import numpy as np
from stt import Model
import time

MODEL_PATH = 'model.tflite'
RECORDING_PATH = 'Spracheingabe.wav'

def create_audio(time):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    record_seconds = time
    file_name = "Spracheingabe.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format = format,
                    channels = channels,
                    rate = rate,
                    input = True,
                    frames_per_buffer = chunk)

    print("Aufnahme gestartet")

    frames = []

    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("Aufnahme beendet")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    return file_name

def convert(model_path, recording_path):
    lm = Model(MODEL_PATH)
    fin = wave.open(RECORDING_PATH, 'rb')
    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
    output = lm.stt(audio)
    return output

create_audio(5)
time.sleep(2)
print(convert('MODEL_PATH', 'RECORDING_PATH'))
