from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import tempfile
import librosa
import soundfile as sf

def speedup_audio(audio_file: InMemoryUploadedFile, speed_factor: float) -> str:
    """
    Speeds up the audio by the specified speed factor.

    :param audio_file: Uploaded audio file
    :param speed_factor: Factor by which to speed up the audio (e.g., 1.5 for 1.5x speed)
    :return: Path to the sped-up audio file
    """
    # Generate a temporary path to save the uploaded file
    temp_input_path = os.path.join(os.getcwd(), audio_file.name)
    temp_input_path = os.path.normpath(temp_input_path)

    # Save the uploaded file to a temporary location
    with open(temp_input_path, "wb") as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)

    # Load the audio file
    y, sr = librosa.load(temp_input_path)

    # Apply speed-up effect (rate=1/speed_factor for time stretching)
    y_sped_up = librosa.effects.time_stretch(y, rate=speed_factor)

    # Save the processed audio to a new temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_output_file:
        temp_output_path = temp_output_file.name
        sf.write(temp_output_path, y_sped_up, sr)

    # Remove the original uploaded file
    os.remove(temp_input_path)

    # Return the path to the processed file
    return temp_output_path
