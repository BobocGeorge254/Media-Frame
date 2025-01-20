import os
import tempfile
from django.core.files.uploadedfile import InMemoryUploadedFile
import librosa
import soundfile as sf
from unittest import TestCase, mock
from io import BytesIO
from processor.transcription import speedup_audio

class TestSpeedupAudio(TestCase):
    @mock.patch("processor.audio_processor.librosa.load")
    @mock.patch("processor.audio_processor.sf.write")
    def test_speedup_audio(self, mock_sf_write, mock_librosa_load):
        # Mock input audio file
        mock_audio_data = [0.1, 0.2, 0.3]  # Dummy audio data
        mock_sr = 22050  # Sample rate
        mock_librosa_load.return_value = (mock_audio_data, mock_sr)

        # Prepare mock InMemoryUploadedFile
        audio_content = BytesIO(b"Dummy audio data")
        uploaded_file = InMemoryUploadedFile(audio_content, None, "test_audio.mp3", "audio/mp3", len(audio_content.getvalue()), None)

        # Call the speedup_audio function
        speed_factor = 1.5
        result_path = speedup_audio(uploaded_file, speed_factor)

        # Verify librosa.load was called with the correct arguments
        mock_librosa_load.assert_called_with(os.path.normpath(os.path.join(os.getcwd(), "test_audio.mp3")))

        # Verify the result file is saved
        mock_sf_write.assert_called()

        # Ensure the function returns the correct path format
        self.assertTrue(result_path.endswith(".mp3"))

        # Clean up the temporary file
        if os.path.exists(result_path):
            os.remove(result_path)

    def test_invalid_speed_factor(self):
        # Mock InMemoryUploadedFile
        audio_content = BytesIO(b"Dummy audio data")
        uploaded_file = InMemoryUploadedFile(audio_content, None, "test_audio.mp3", "audio/mp3", len(audio_content.getvalue()), None)

        # Check for errors if the speed factor is invalid
        with self.assertRaises(ValueError):
            speedup_audio(uploaded_file, -1)  # Negative speed factor should raise an error
