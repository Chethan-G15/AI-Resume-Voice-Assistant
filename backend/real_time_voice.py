import sounddevice as sd
import numpy as np
import whisper
import wave
import threading


SAMPLE_RATE = 16000
CHANNELS = 1
MICROPHONE_DEVICE = 1

recording = True
audio_data = []


print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper loaded successfully!")


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


thread = threading.Thread(target=record_audio)

thread.start()

input()

recording = False

thread.join()


print("\nRecording completed.")
print("Preparing audio...")


audio = np.concatenate(audio_data, axis=0)


with wave.open("voice_query.wav", "wb") as wf:

    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)

    wf.writeframes(audio.tobytes())


print("Transcribing...")


result = model.transcribe("voice_query.wav")

text = result["text"].strip()


print("\nVoice Query:")
print(text)