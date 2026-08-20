import whisper

print("Loading Whisper model...")

model = whisper.load_model("base")

print("Transcribing audio...")

result = model.transcribe("audio.wav")

print("Transcription:")
print(result["text"])