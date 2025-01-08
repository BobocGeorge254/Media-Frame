from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import tempfile
import librosa
import soundfile as sf
import numpy as np

def bassboost_audio(audio_file: InMemoryUploadedFile) -> str:
    # Generate a temporary path to save the uploaded file
    temp_input_path = os.path.join(os.getcwd(), audio_file.name)
    temp_input_path = os.path.normpath(temp_input_path)

    # Save the uploaded file to a temporary location
    with open(temp_input_path, "wb") as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)

    # Load the audio file
    y, sr = librosa.load(temp_input_path)

    # Apply bass boosting by amplifying low frequencies
    fft = np.fft.fft(y)
    frequencies = np.fft.fftfreq(len(fft), d=1/sr)

    # Amplify low frequencies (below 150 Hz)
    bass_boost_filter = (frequencies > 0) & (frequencies < 150)
    fft[bass_boost_filter] *= 2.0  # Boost low frequencies by 2x
    y_boosted = np.fft.ifft(fft).real

    # Save the processed audio to a new temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_output_file:
        temp_output_path = temp_output_file.name
        sf.write(temp_output_path, y_boosted, sr)

    # Remove the original uploaded file
    os.remove(temp_input_path)

    # Return the path to the processed file
    return temp_output_path
