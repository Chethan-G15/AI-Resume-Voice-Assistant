import sounddevice as sd
import numpy as np
import wave
import requests
import threading


SAMPLE_RATE = 16000
CHANNELS = 1
MICROPHONE_DEVICE = 1

API_URL = "http://127.0.0.1:8000/voice/query"

recording = True
audio_data = []


def record_audio():

    global recording

    print("\n🎤 Speak your question...")
    print("Press ENTER when you finish speaking.\n")

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        device=MICROPHONE_DEVICE
    )

    with stream:

        while recording:

            data, overflowed = stream.read(1024)

            audio_data.append(data.copy())


# Start recording in background
thread = threading.Thread(target=record_audio)

thread.start()

# Wait for user to press Enter
input()

recording = False

thread.join()


print("\nRecording completed.")


# Convert recorded audio
audio = np.concatenate(audio_data, axis=0)
# Normalize microphone volume
audio = audio.astype(np.float32)

max_value = np.max(np.abs(audio))

if max_value > 0:
    audio = audio / max_value

audio = (audio * 32767).astype(np.int16)


audio_file = "voice_query.wav"


with wave.open(audio_file, "wb") as wf:

    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)

    wf.writeframes(audio.tobytes())


print("Sending voice query to API...")


# Send audio to FastAPI
with open(audio_file, "rb") as file:

    response = requests.post(
        API_URL,
        files={
            "file": (
                audio_file,
                file,
                "audio/wav"
            )
        }
    )


print("\nAPI Response:")

print(response.json())