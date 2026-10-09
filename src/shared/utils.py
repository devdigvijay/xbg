from assemblyai.streaming.v3 import (
    BeginEvent,
    RealTimeError,
    RealTimeTranscriber,
    TerminationEvent,
    TurnEvent,
)


def on_begin(client: RealTimeTranscriber, event: BeginEvent):
    print(f"Session started: {event.id}")

def on_turn(client: RealTimeTranscriber, event: TurnEvent):
    if event.end_of_turn and event.transcript.strip():
        print(f"{event.transcript}")

def on_terminated(client: RealTimeTranscriber, event: TerminationEvent):
    print(f"Session terminated: {event.audio_duration_seconds} seconds of audio processed")

def on_error(client: RealTimeTranscriber, error: RealTimeError):
    print(f"Error occurred: {error}")
