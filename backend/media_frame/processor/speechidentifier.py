from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import tempfile
import whisper

def speechidentifier_audio(audio_file: InMemoryUploadedFile) -> dict:
    # Generate a temporary path to save the uploaded file
    temp_input_path = os.path.join(os.getcwd(), audio_file.name)
    temp_input_path = os.path.normpath(temp_input_path)

    # Save the uploaded file to a temporary location
    with open(temp_input_path, "wb") as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)

    # Load the Whisper model
    model = whisper.load_model("base")

    # Transcribe the audio
    result = model.transcribe(temp_input_path)

    # Remove the original uploaded file
    os.remove(temp_input_path)

    # Return the transcription result
    return result
