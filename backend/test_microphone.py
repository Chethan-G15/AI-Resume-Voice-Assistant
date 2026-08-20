import sounddevice as sd
import numpy as np
import whisper
import wave


SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 7
MICROPHONE_DEVICE = 1


print("Loading Whisper model...")

model = whisper.load_model("base")

print("Whisper loaded successfully!")
print("\nSpeak clearly for 7 seconds...")
print("Say:")
print("What are Chethan's skills?")
print("\nRecording...")


audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="float32",
    device=MICROPHONE_DEVICE
)

sd.wait()


# Convert float audio to 16-bit PCM
audio = np.clip(audio, -1, 1)

audio_int16 = (audio * 32767).astype(np.int16)


with wave.open("test_voice.wav", "wb") as wf:

    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)

    wf.writeframes(audio_int16.tobytes())


print("\nRecording completed.")
print("Transcribing...")


result = model.transcribe(
    "test_voice.wav",
    language="en",
    fp16=False
)


text = result["text"].strip()


print("\nWhisper heard:")
print(text)