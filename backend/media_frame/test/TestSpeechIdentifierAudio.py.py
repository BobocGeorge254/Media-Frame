import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from processor.speechidentifier import speechidentifier_audio


class TestSpeechIdentifierAudio(unittest.TestCase):

    @patch('librosa.load')
    @patch('librosa.feature.mfcc')
    @patch('sklearn.cluster.KMeans')
    @patch('whisper.load_model')
    def test_speechidentifier_audio(self, mock_whisper_model, mock_kmeans, mock_mfcc, mock_librosa_load):
        # Simulate loading audio with librosa
        y = np.random.rand(22050)  # Simulate a 1-second audio file at 22050 Hz
        sr = 22050  # Sampling rate
        mock_librosa_load.return_value = (y, sr)

        # Simulate MFCC extraction
        mfcc = np.random.rand(10, 13)  # 10 frames, 13 MFCC coefficients
        mock_mfcc.return_value = mfcc

        # Simulate KMeans clustering (2 speakers in this case)
        mock_kmeans_instance = mock_kmeans.return_value
        mock_kmeans_instance.fit_predict.return_value = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]  # Labels simulate 2 speakers

        # Simulate Whisper transcription
        mock_whisper_instance = mock_whisper_model.return_value
        mock_whisper_instance.transcribe.return_value = {
            "text": "Hello world",
            "segments": [
                {"start": 0.0, "end": 0.5, "text": "Hello"},
                {"start": 0.5, "end": 1.0, "text": "world"}
            ]
        }

        # Simulate an audio file uploaded in memory
        audio_data = BytesIO(b"fake_audio_data")
        audio_file = InMemoryUploadedFile(audio_data, 'audio', 'test_audio.wav', 'audio/wav', len(audio_data.getvalue()), None)

        # Call the function under test
        result = speechidentifier_audio(audio_file)

        # Check if the transcription and speaker segments are correct
        self.assertEqual(result['transcription'], "Hello world")

        # Verify speaker segments
        speaker_segments = result['speaker_segments']
        self.assertEqual(len(speaker_segments), 3)
        self.assertEqual(speaker_segments[0]['speaker'], "Speaker 1")
        self.assertIn("Hello", speaker_segments[0]['text'])  # Ensure "Hello" is assigned to Speaker 1
        self.assertEqual(speaker_segments[1]['speaker'], "Speaker 2")
        self.assertIn("world", speaker_segments[1]['text'])  # Ensure "world" is assigned to Speaker 2

    @patch('os.remove')
    @patch('os.path.exists')
    @patch('librosa.load')
    def test_cleanup_temp_file(self, mock_librosa_load, mock_os_path_exists, mock_os_remove):
        # Simulate the temporary file existence
        mock_os_path_exists.return_value = True

        # Force an exception in librosa.load to trigger the 'finally' block
        mock_librosa_load.side_effect = Exception("Librosa error")

        # Simulate an audio file uploaded in memory
        audio_data = BytesIO(b"fake_audio_data")
        audio_file = InMemoryUploadedFile(audio_data, 'audio', 'test_audio.wav', 'audio/wav', len(audio_data.getvalue()), None)

        # Call the function and expect an exception
        with self.assertRaises(Exception):
            speechidentifier_audio(audio_file)

        # Ensure the temporary file is deleted after an error
        mock_os_remove.assert_called_once()

if __name__ == '__main__':
    unittest.main()
