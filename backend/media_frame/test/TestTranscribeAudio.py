import os
import tempfile
from django.core.files.uploadedfile import InMemoryUploadedFile
from unittest import TestCase, mock
from io import BytesIO
import librosa
import soundfile as sf
from processor.speedup import speedup_audio

class TestSpeedupAudio(TestCase):

    @mock.patch("processor.audio_processor.librosa.load")
    @mock.patch("processor.audio_processor.librosa.effects.time_stretch")
    @mock.patch("processor.audio_processor.sf.write")
    def test_speedup_audio(self, mock_sf_write, mock_time_stretch, mock_librosa_load):
        # Mock audio data
        y = [0.1, 0.2, 0.3]
        sr = 22050
        mock_librosa_load.return_value = (y, sr)
        
        # Mock speed-up processing result
        y_sped_up = [0.2, 0.3, 0.4]
        mock_time_stretch.return_value = y_sped_up

        # Prepare mock InMemoryUploadedFile
        audio_content = BytesIO(b"Dummy audio data")
        uploaded_file = InMemoryUploadedFile(audio_content, None, "test_audio.mp3", "audio/mp3", len(audio_content.getvalue()), None)

        # Call the speedup_audio function
        result_file_path = speedup_audio(uploaded_file, speed_factor=1.5)

        # Assert librosa.load was called
        mock_librosa_load.assert_called_once_with(mock.ANY)

        # Assert librosa.effects.time_stretch was called with the correct arguments
        mock_time_stretch.assert_called_once_with(y, rate=1.5)

        # Assert sf.write was called to save the sped-up audio
        mock_sf_write.assert_called_once_with(result_file_path, y_sped_up, sr)

        # Assert the returned file path is valid
        self.assertTrue(os.path.exists(result_file_path))

        # Clean up the generated temporary file
        if os.path.exists(result_file_path):
            os.remove(result_file_path)

    def test_cleanup_after_processing(self):
        # Mock InMemoryUploadedFile
        audio_content = BytesIO(b"Dummy audio data")
        uploaded_file = InMemoryUploadedFile(audio_content, None, "test_audio.mp3", "audio/mp3", len(audio_content.getvalue()), None)

        # Mock librosa and sf to avoid actual audio processing
        with mock.patch("processor.audio_processor.librosa.load"), \
             mock.patch("processor.audio_processor.librosa.effects.time_stretch"), \
             mock.patch("processor.audio_processor.sf.write"):

            # Call the function
            result_file_path = speedup_audio(uploaded_file, speed_factor=1.5)

            # Ensure the original uploaded file is removed
            temp_input_path = os.path.join(os.getcwd(), uploaded_file.name)
            self.assertFalse(os.path.exists(temp_input_path), "Original uploaded file was not removed.")

            # Clean up the generated file
            if os.path.exists(result_file_path):
                os.remove(result_file_path)

    def test_temp_file_cleanup(self):
        # Mock InMemoryUploadedFile
        audio_content = BytesIO(b"Dummy audio data")
        uploaded_file = InMemoryUploadedFile(audio_content, None, "test_audio.mp3", "audio/mp3", len(audio_content.getvalue()), None)

        # Mock librosa and sf to avoid actual audio processing
        with mock.patch("processor.audio_processor.librosa.load"), \
             mock.patch("processor.audio_processor.librosa.effects.time_stretch"), \
             mock.patch("processor.audio_processor.sf.write"):

            # Call the function
            result_file_path = speedup_audio(uploaded_file, speed_factor=1.5)

            # Check if temporary files are cleaned up
            temp_dir = tempfile.gettempdir()
            temp_files = [f for f in os.listdir(temp_dir) if f.endswith(".mp3")]
            self.assertEqual(len(temp_files), 0, "Temporary file was not deleted.")

            # Clean up the generated file
            if os.path.exists(result_file_path):
                os.remove(result_file_path)
