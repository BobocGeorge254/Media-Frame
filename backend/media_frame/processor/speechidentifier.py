from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import librosa
import numpy as np
from sklearn.cluster import KMeans
import whisper

def speechidentifier_audio(audio_file: InMemoryUploadedFile) -> dict:
    # Save the uploaded audio file temporarily
    temp_input_path = os.path.join(os.getcwd(), audio_file.name)
    temp_input_path = os.path.normpath(temp_input_path)

    with open(temp_input_path, "wb") as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)

    try:
        # Load the audio file and extract features
        y, sr = librosa.load(temp_input_path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc = mfcc.T  # Transpose for clustering (time x features)

        # Perform clustering on the MFCC features
        n_speakers = 2  # Change this based on the expected number of speakers
        kmeans = KMeans(n_clusters=n_speakers, random_state=42)
        labels = kmeans.fit_predict(mfcc)

        # Reconstruct speaker segments
        hop_length = 512  # Default librosa hop length
        frame_duration = hop_length / sr
        speaker_segments = []
        current_speaker = labels[0]
        start_time = 0

        for i in range(1, len(labels)):
            if labels[i] != current_speaker:
                end_time = i * frame_duration
                speaker_segments.append({
                    "start_time": start_time,
                    "end_time": end_time,
                    "speaker": f"Speaker {current_speaker + 1}",
                    "text": ""  # Placeholder for text
                })
                current_speaker = labels[i]
                start_time = end_time

        # Append the last segment
        speaker_segments.append({
            "start_time": start_time,
            "end_time": len(y) / sr,
            "speaker": f"Speaker {current_speaker + 1}",
            "text": ""
        })

        # Transcribe the audio using Whisper
        whisper_model = whisper.load_model("base")
        transcription_result = whisper_model.transcribe(temp_input_path, word_timestamps=True)

        # Align text with speaker segments
        words = transcription_result["segments"]
        for word_segment in words:
            word_start = word_segment["start"]
            word_end = word_segment["end"]
            word_text = word_segment["text"]

            # Find the corresponding speaker segment for this word
            for segment in speaker_segments:
                if segment["start_time"] <= word_start < segment["end_time"]:
                    segment["text"] += f" {word_text}"  # Append the word to the segment text
                    break

        # Filter out segments with no text
        speaker_segments = [seg for seg in speaker_segments if seg["text"].strip()]

        return {
            "transcription": transcription_result["text"],
            "speaker_segments": speaker_segments
        }
    finally:
        # Clean up temporary file
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)
