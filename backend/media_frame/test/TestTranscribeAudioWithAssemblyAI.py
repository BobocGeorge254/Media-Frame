import unittest
from unittest.mock import patch, MagicMock
from processor.transcription_video import transcribe_audio_with_assemblyai


class TestTranscribeAudioWithAssemblyAI(unittest.TestCase):
    @patch('processor.video_processor.aai.Transcriber')
    def test_transcribe_audio_success(self, mock_transcriber):
        # Mocking AssemblyAI transcription response
        mock_transcription = MagicMock()
        mock_transcription.words = [
            {'start': 0.0, 'end': 1.0, 'text': 'Hello'},
            {'start': 1.0, 'end': 2.0, 'text': 'world'}
        ]
        mock_transcription.status = 'completed'
        mock_transcriber.return_value.transcribe.return_value = mock_transcription

        result = transcribe_audio_with_assemblyai('audio_file_path.mp3')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['text'], 'Hello')

    @patch('processor.video_processor.aai.Transcriber')
    def test_transcribe_audio_error(self, mock_transcriber):
        # Simulate transcription failure
        mock_transcription = MagicMock()
        mock_transcription.status = 'error'
        mock_transcriber.return_value.transcribe.return_value = mock_transcription

        with self.assertRaises(RuntimeError):
            transcribe_audio_with_assemblyai('audio_file_path.mp3')
