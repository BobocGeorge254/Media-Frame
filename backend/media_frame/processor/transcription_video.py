import os
import cv2
import assemblyai as aai
from moviepy.editor import VideoFileClip

aai.settings.api_key = "2e7cd914329f43cd86f2ee5a1765ba3c"

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

    return transcript.words  # Returns a list of `Word` objects

def add_subtitles_to_video(video_path: str, segments: list) -> str:
    """
    Add subtitles to the video using OpenCV based on transcription segments.
    """
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_video_path = video_path.replace(".mp4", "_subtitled.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4 codec
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    frame_number = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    word_frame_mapping = []
    for word in segments:
        start_frame = int((word.start / 1000) * fps) 
        end_frame = int((word.end / 1000) * fps)
        word_frame_mapping.append((start_frame, end_frame, word.text))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for start_frame, end_frame, text in word_frame_mapping:
            if start_frame <= frame_number <= end_frame:
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                color = (255, 255, 255)  
                thickness = 2
                position = (50, height - 50)  

                wrapped_text = wrap_text(text, width, font, font_scale, thickness)

                y_offset = height - 50
                for line in wrapped_text:
                    cv2.putText(frame, line, (50, y_offset), font, font_scale, color, thickness, lineType=cv2.LINE_AA)
                    y_offset += 30  

        out.write(frame)
        frame_number += 1

    cap.release()
    out.release()

    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    final_video = VideoFileClip(output_video_path)

    final_video = final_video.set_audio(audio_clip)

    final_output_path = video_path.replace(".mp4", "_final.mp4")
    final_video.write_videofile(final_output_path, codec="libx264", audio_codec="aac", fps=fps)

    return final_output_path

def wrap_text(text, max_width, font, font_scale, thickness):
    """
    Wrap text to fit within the width of the screen, ensuring each line fits
    """
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        text_size = cv2.getTextSize(test_line, font, font_scale, thickness)[0]
        text_width = text_size[0]

        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines
