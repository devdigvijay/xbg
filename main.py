import os
from src.transcribe.audio import microphone_stream
from dotenv import load_dotenv
from src.shared.utils import (
    on_begin,
    on_turn,
    on_terminated,
    on_error
) 
from assemblyai.streaming.v3 import (
    RealTimeEvents,
    RealTimeParameters,
    RealTimeTranscriber,
    RealTimeTranscriberOptions,
)

load_dotenv()
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

def main():
    client = RealTimeTranscriber(
            RealTimeTranscriberOptions(
                api_key=API_KEY,
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
        client.stream(microphone_stream())
    finally:
        client.disconnect(terminate=True)

if __name__ == "__main__":
    main()