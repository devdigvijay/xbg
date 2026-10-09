# Live Speech Transcription

A small Python command-line app that captures audio from the default microphone and sends it to AssemblyAI's real-time transcription service. Completed speech turns are printed in the terminal.

## What runs

The supported entry point is `main.py`. It:

1. Loads configuration from `.env`.
2. Opens the default microphone as mono, signed 16-bit PCM audio.
3. Connects to AssemblyAI's streaming service using the `universal-3-6-pro` speech model.
4. Streams audio in 50 ms frames and prints completed transcript turns.
5. Disconnects the streaming session and releases the microphone when the stream ends or you press **Ctrl+C**.

This is a synchronous, blocking command-line program; it does not provide an `asyncio` interface or a graphical user interface. The other source files include supporting callbacks and an experimental internet-radio example; they are not required to run the microphone app.

## Requirements

- Windows, macOS, or Linux with Python **3.13** (the project currently requires `>=3.13,<3.14`).
- A working microphone and permission for the terminal/Python process to access it.
- An AssemblyAI API key. Audio is sent to AssemblyAI for transcription; network access is required.
- [uv](https://docs.astral.sh/uv/) is recommended. A regular Python virtual environment and pip can also be used.

## Setup

### With uv

From the repository root:

```powershell
uv sync
Copy-Item .env.example .env
```

Edit `.env` and replace the placeholder API key with your key. Then start the app:

```powershell
uv run python main.py
```

### With Python and pip

Create and activate a Python 3.13 virtual environment, then install the project:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
Copy-Item .env.example .env
```

Edit `.env`, then run:

```powershell
python main.py
```

On macOS or Linux, use the platform's equivalent virtual-environment activation and file-copy commands. PyAudio depends on the operating system's audio support; if its installation fails, install the appropriate PortAudio/PyAudio system prerequisites for your platform and retry.

## Configuration

`.env.example` is the template. Copy it to `.env` in the repository root and use plain `KEY=value` lines (no angle brackets and no surrounding quotes are needed for these values):

| Variable | Required | Meaning |
| --- | --- | --- |
| `ASSEMBLYAI_API_KEY` | Yes | API key used to authenticate the real-time transcription session. |
| `SAMPLE_RATE` | Yes | Microphone sample rate in Hz. The current streaming connection is configured for 16,000 Hz; keep this value at `16000` so the captured audio and service settings agree. |
| `FRAMES_PER_BUFFER` | Yes | Number of audio frames captured per read. `800` frames at 16,000 Hz is 50 ms of audio. |

Keep `.env` private. It is ignored by Git; do not paste API keys into source files, commit them, or share them in logs or screenshots. If a key has been exposed, revoke it in the AssemblyAI dashboard and create a replacement.

## Using the app

Run `uv run python main.py` (or `python main.py` in the activated environment), speak into the default microphone, and read completed transcript turns in the terminal. Press **Ctrl+C** to stop. The `finally` cleanup disconnects the transcription session; the audio generator also closes the microphone stream when it is stopped.

`FRAMES_PER_BUFFER` controls the size of each microphone read, not the total recording duration. Larger values send audio in larger batches; smaller values send more frequent batches. The app runs until interrupted and does not currently save audio or transcripts to files.

## Troubleshooting and edge cases

- **Missing or rejected API key:** Check that `.env` exists in the repository root and contains `ASSEMBLYAI_API_KEY=...` with a valid key. An empty, placeholder, expired, or revoked key prevents authentication.
- **Missing or invalid audio settings:** `SAMPLE_RATE` and `FRAMES_PER_BUFFER` must both be present and parse as integers because the microphone setup reads them at startup. Keep `SAMPLE_RATE=16000` to match the streaming connection, and use a positive buffer size such as `800`.
- **Microphone not found, denied, or in use:** Select/enable a default input device, grant microphone permission to the terminal or IDE, and close other programs that exclusively use the device. The app captures from the system's default microphone; it has no device-selection UI.
- **No transcript appears:** Confirm that the session-start message appears, the correct microphone is selected, its input level is nonzero, and the network can reach AssemblyAI. The callback prints only completed, non-empty turns, so partial speech may not appear immediately.
- **Connection or service errors:** Check internet access, the API key, and the AssemblyAI service status. Streaming errors are printed by the registered error callback. The app does not currently retry a failed connection automatically.
- **Audio overflow or choppy capture:** The microphone reader suppresses PyAudio's overflow exception, but lost audio cannot be recovered. Close CPU-heavy applications and check the input device. Adjust the buffer only if necessary; keep the configured sample rate in agreement with the streaming parameters.
- **Stopping the process:** Use **Ctrl+C** for a normal stop so the disconnect and microphone cleanup code can run. Force-closing the terminal or killing the process cannot guarantee cleanup.
- **No display / headless environment:** This entry point is terminal-based and does not open a GUI. A microphone device is still required.
- **Windows PowerShell does not allow activation:** You can avoid activation and run commands through uv (`uv run python main.py`), or use the virtual environment interpreter directly (`.\.venv\Scripts\python.exe main.py`).

## Project layout

| Path | Purpose |
| --- | --- |
| `main.py` | Main microphone transcription entry point and event-handler registration. |
| `src/transcribe/audio.py` | Opens the default microphone and yields audio frames. |
| `src/shared/utils.py` | Prints session, transcript-turn, termination, and error events. |
| `src/transcribe/transcribe.py` | Experimental internet-radio streaming example; it requires a reachable radio stream and is separate from the microphone entry point. |
| `demo.py` | Standalone microphone example. |
| `.env.example` | Safe configuration template to copy to `.env`. |
| `pyproject.toml` / `uv.lock` | Project metadata, dependency declarations, Python version, and locked dependency versions. |

## Development notes

- The configured model and sample rate are set in `main.py`; the microphone format is mono, signed 16-bit PCM.
- No automated test suite is currently included in the repository.
- `pyside6` and `pyinstaller` are listed project dependencies, but the current entry point does not launch a GUI or build a packaged executable.

## License

See [LICENSE.txt](LICENSE.txt).
