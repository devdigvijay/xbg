import os
import pyaudio
from dotenv import load_dotenv
load_dotenv()

SAMPLE_RATE = int(os.getenv("SAMPLE_RATE"))
FRAMES_PER_BUFFER = int(os.getenv("FRAMES_PER_BUFFER"))

def microphone_stream():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER,
    )
    try:
        while True:
            yield stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
