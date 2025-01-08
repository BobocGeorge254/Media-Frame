import tempfile
import os
from django.core.files.uploadedfile import InMemoryUploadedFile

def transcribe_audio(audio_file: InMemoryUploadedFile) -> str:
    global model

    if model is None:
        raise RuntimeError("Whisper model is not loaded.")

    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)
        temp_file.flush()
        temp_file_path = temp_file.name

    # Ensure the file exists
    if not os.path.exists(temp_file_path):
        raise FileNotFoundError(f"Temporary file not found: {temp_file_path}")

    # Use the temporary file path for transcription
    try:
        result = model.transcribe(temp_file_path)
        return result["text"]
    finally:
        # Clean up the temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)