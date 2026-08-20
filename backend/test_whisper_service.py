from app.services.whisper_service import transcribe_audio


audio_file = "audio.wav"

text = transcribe_audio(audio_file)

print("Voice Query:")
print(text)