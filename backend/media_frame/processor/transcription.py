from django.core.files.uploadedfile import InMemoryUploadedFile
import tempfile
import os

def transcribe_audio(audio_file: InMemoryUploadedFile) -> str:
    global model

    if model is None:
        raise RuntimeError("Whisper model is not loaded.")

    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)
        temp_file.flush()

        # Use the temporary file path for transcription
        result = model.transcribe(temp_file.name)
        return result["text"]
    
    
