import logging
import os

import pyaudio
from dotenv import load_dotenv
from assemblyai.streaming.v3 import (
    BeginEvent,
    RealTimeError,
    RealTimeEvents,
    RealTimeParameters,
    RealTimeTranscriber,
    RealTimeTranscriberOptions,
    TerminationEvent,
    TurnEvent,
)

load_dotenv()
api_key = os.getenv("ASSEMBLYAI_API_KEY")

# The SDK does not capture audio itself: pyaudio reads 16-bit mono PCM from the
# default microphone and the chunks are handed to the transcriber below.
SAMPLE_RATE = 16000
FRAMES_PER_BUFFER = 800  # 50ms of audio per chunk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def on_begin(client: RealTimeTranscriber, event: BeginEvent):
    print(f"Session started: {event.id}")

def on_turn(client: RealTimeTranscriber, event: TurnEvent):
    print(f"{event.transcript} ({event.end_of_turn})")

def on_terminated(client: RealTimeTranscriber, event: TerminationEvent):
    print(
        f"Session terminated: {event.audio_duration_seconds} seconds of audio processed"
    )

def on_error(client: RealTimeTranscriber, error: RealTimeError):
    print(f"Error occurred: {error}")

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

def main():
    if not api_key:
        raise RuntimeError(
            "ASSEMBLYAI_API_KEY is not set. Add it to a .env file or the environment."
        )

    client = RealTimeTranscriber(
        RealTimeTranscriberOptions(
            api_key=api_key,
            api_host="streaming.assemblyai.com",
        )
    )

    client.on(RealTimeEvents.Begin, on_begin)
    client.on(RealTimeEvents.Turn, on_turn)
    client.on(RealTimeEvents.Termination, on_terminated)
    client.on(RealTimeEvents.Error, on_error)

    client.connect(
        RealTimeParameters(
            sample_rate = 16000,
            speech_model = "universal-3-6-pro",
            mode = "balanced"
        )
    )

    try:
        # Stop with Ctrl-C; the session is terminated cleanly in `finally`.
        client.stream(microphone_stream())
    finally:
        client.disconnect(terminate=True)

if __name__ == "__main__":
    main()
