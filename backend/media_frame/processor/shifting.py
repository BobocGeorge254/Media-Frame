from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import tempfile
import librosa
import soundfile as sf

def shift_audio(audio_file: InMemoryUploadedFile, n_steps: int) -> str:
    # Generate a temporary path to save the uploaded file
    temp_input_path = os.path.join(os.getcwd(), audio_file.name)
    temp_input_path = os.path.normpath(temp_input_path)

    # Save the uploaded file to a temporary location
    with open(temp_input_path, "wb") as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)

    # Ensure the file was saved correctly
    if not os.path.exists(temp_input_path):
        raise FileNotFoundError(f"Uploaded file was not saved correctly: {temp_input_path}")

    # Load the audio file
    y, sr = librosa.load(temp_input_path)
    
    # Apply pitch shifting using the provided n_steps
    y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=n_steps)

    # Save the processed audio to a new temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_output_file:
        temp_output_path = temp_output_file.name
        sf.write(temp_output_path, y_shifted, sr)

    # Remove the original uploaded file
    os.remove(temp_input_path)

    # Return the path to the processed file
    return temp_output_path