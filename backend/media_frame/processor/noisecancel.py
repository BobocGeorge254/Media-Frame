import os
import tempfile
import librosa
import soundfile as sf
import numpy as np

def noisecancel_audio(audio_file):
    # Generate a temporary path to save the uploaded file
    temp_input_path = os.path.join(os.getcwd(), audio_file.name)
    temp_input_path = os.path.normpath(temp_input_path)

    # Save the uploaded file to a temporary location
    with open(temp_input_path, "wb") as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)

    # Load the audio file
    y, sr = librosa.load(temp_input_path)

    # Generate a noise profile by taking the quieter parts of the signal
    # Here, we assume the first second is noise (adjust as needed)
    noise_duration = min(len(y) // sr, 1)  # Use the first second or available duration
    noise_sample = y[:noise_duration * sr]

    # Compute the noise profile
    noise_spectrum = np.abs(librosa.stft(noise_sample, n_fft=2048, hop_length=512))
    noise_profile = np.mean(noise_spectrum, axis=1)

    # Perform noise cancellation using spectral gating
    y_stft = librosa.stft(y, n_fft=2048, hop_length=512)
    y_magnitude, y_phase = librosa.magphase(y_stft)

    # Subtract the noise profile
    y_magnitude_cleaned = np.maximum(y_magnitude - noise_profile[:, np.newaxis], 0)

    # Reconstruct the audio using the cleaned magnitude and original phase
    y_cleaned = librosa.istft(y_magnitude_cleaned * y_phase, hop_length=512)

    # Save the cleaned audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_output_file:
        temp_output_path = temp_output_file.name
        sf.write(temp_output_path, y_cleaned, sr)

    # Remove the original uploaded file
    os.remove(temp_input_path)

    # Return the path to the processed file
    return temp_output_path
