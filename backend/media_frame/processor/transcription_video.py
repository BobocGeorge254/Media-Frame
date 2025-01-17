import os
import tempfile
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import assemblyai as aai

# Set your AssemblyAI API key
aai.settings.api_key = "2e7cd914329f43cd86f2ee5a1765ba3c"

# Path to the custom font
current_directory = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(current_directory, "font.ttf")

def transcribe_audio_with_assemblyai(file_path: str) -> list:
    """
    Transcribe audio using AssemblyAI from a local file path and return timestamped segments.
    """
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription error: {transcript.error}")

    # Extract timestamped words
    return transcript.words  # Returns a list of words with start/end times


def add_subtitles_to_video(video_path: str, segments: list) -> str:
    """
    Add subtitles dynamically to the video using moviepy based on transcription segments.
    """
    # Load the video
    video = VideoFileClip(video_path)

    # Generate TextClips for each segment
    subtitle_clips = []
    for segment in segments:
        start_time = segment["start"] / 1000.0  # Convert milliseconds to seconds
        end_time = segment["end"] / 1000.0  # Convert milliseconds to seconds
        text = segment["text"]

        # Create a TextClip for the current segment
        subtitle = TextClip(
            text=text,
            font=font_path,
            fontsize=30,
            color="white",
            bg_color="black",
            stroke_color="yellow",  # Optional stroke for better visibility
            stroke_width=1,
            method="caption",
            size=(video.size[0] - 100, None),  # Subtitle width with padding
            text_align="center",
            interline=4,  # Spacing between lines
        ).set_start(start_time).set_end(end_time).set_position(("center", "bottom"))

        subtitle_clips.append(subtitle)

    # Combine video and subtitles
    final_video = CompositeVideoClip([video, *subtitle_clips])
    output_video_path = video_path.replace(".mp4", "_subtitled.mp4")
    final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac", fps=24)

    return output_video_path


# Example usage
if __name__ == "__main__":
    video_file_path = "path/to/video.mp4"  # Replace with your video file path
    audio_file_path = "path/to/audio.mp3"  # Replace with your audio file path (if needed)

    # Transcribe the audio and get timestamped segments
    segments = transcribe_audio_with_assemblyai(audio_file_path)

    # Add subtitles to the video
    subtitled_video = add_dynamic_subtitles_to_video(video_file_path, segments)
    print(f"Subtitled video saved to: {subtitled_video}")