import whisper


MODEL_NAME = "base"

model = whisper.load_model(MODEL_NAME)


def transcribe_audio(file_path: str) -> str:
    result = model.transcribe(file_path)

    return result["text"].strip()