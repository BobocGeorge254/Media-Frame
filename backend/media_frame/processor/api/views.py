import os
import tempfile
from django.http import FileResponse
from processor.transcription_video import add_subtitles_to_video, transcribe_audio_with_assemblyai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from processor.transcription import transcribe_audio
from processor.shifting import shift_audio
from processor.noisecancel import noisecancel_audio
from processor.bassboost import bassboost_audio
from processor.speechidentifier import speechidentifier_audio
from processor.speedup import speedup_audio
from authentication.models import CustomUser, Tier
from rest_framework import permissions
from processor.models import ProcessorUsage
from django.utils import timezone
from .serializer import ProcessorUsageSerializer
from django.utils.timezone import now


class TranscriptionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')
        language = request.data.get('language', 'en')  # Default to English if not provided

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.has_reached_limit(request.user):
            return Response(
                {"error": "You have reached your daily processing limit."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if CustomUser.objects.get_user_tier(request.user) == Tier.FREE:
            return Response(
                {"error": "You don't have permission to make this operation."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            transcript = transcribe_audio(audio_file, language)

            ProcessorUsage.objects.create(
                user=request.user,
                processor_type='transcription',
                file=audio_file,
                timestamp=timezone.now()
            )

            return Response({"transcript": transcript}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class PitchShiftingAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        
        audio_file = request.FILES.get('file')

        if CustomUser.objects.has_reached_limit(request.user):
            return Response(
                {"error": "You have reached your daily processing limit."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if CustomUser.objects.get_user_tier(request.user) == Tier.FREE:
            return Response(
                {"error": "You don't have permission to make this operation."},
                status=status.HTTP_403_FORBIDDEN
            )

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extract n_steps from the request, default to 2 if not provided
            n_steps = request.data.get('n_steps', 2)
            try:
                n_steps = int(n_steps)  # Convert to integer
            except ValueError:
                return Response({"error": "Invalid value for n_steps, must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

            # Perform pitch shifting
            new_audio_path = shift_audio(audio_file, n_steps)

            ProcessorUsage.objects.create(
                user=request.user,
                processor_type='pitch_shift',
                file=audio_file,
                timestamp=timezone.now()
            )

            # Serve the pitch-shifted audio file as a download
            response = FileResponse(open(new_audio_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="shifted_audio.mp3"'

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class NoiseCancelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.has_reached_limit(request.user):
            return Response(
                {"error": "You have reached your daily processing limit."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Perform noise cancellation
            new_audio_path = noisecancel_audio(audio_file)

            ProcessorUsage.objects.create(
                user=request.user,
                processor_type='noise_cancel',
                file=audio_file,
                timestamp=timezone.now()
            )


            # Serve the noise-canceled audio file as a download
            response = FileResponse(open(new_audio_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="noisecancelled_audio.mp3"'

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BassBoostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.has_reached_limit(request.user):
            return Response(
                {"error": "You have reached your daily processing limit."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Perform bass boosting
            new_audio_path = bassboost_audio(audio_file)

            ProcessorUsage.objects.create(
                user=request.user,
                processor_type='bass_boost',
                file=audio_file,
                timestamp=timezone.now()
            )

            # Serve the bass-boosted audio file as a download
            response = FileResponse(open(new_audio_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="bassboosted_audio.mp3"'

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SpeechIdentifierAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.has_reached_limit(request.user):
            return Response(
                {"error": "You have reached your daily processing limit."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if CustomUser.objects.get_user_tier(request.user) == Tier.FREE:
            return Response(
                {"error": "You don't have permission to make this operation."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Identify speech in the audio file
            speech_info = speechidentifier_audio(audio_file)

            ProcessorUsage.objects.create(
                user=request.user,
                processor_type='speech_identifier',
                file=audio_file,
                timestamp=timezone.now()
            )

            return Response({"speech_info": speech_info}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SpeedUpAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.has_reached_limit(request.user):
            return Response(
                {"error": "You have reached your daily processing limit."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        
        if CustomUser.objects.get_user_tier(request.user) == Tier.FREE:
            return Response(
                {"error": "You don't have permission to make this operation."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Get the speed factor from the request (default to 1.5 if not provided)
            speed_factor = float(request.data.get('speed_factor', 1.5))

            # Perform speed-up
            new_audio_path = speedup_audio(audio_file, speed_factor)

            ProcessorUsage.objects.create(
                user=request.user,
                processor_type='speed_up',
                file=audio_file,
                timestamp=timezone.now()
            )


            # Serve the processed audio file as a download
            response = FileResponse(open(new_audio_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="speedup_audio.mp3"'

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ProcessorUsageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        processor_usages = ProcessorUsage.objects.filter(user=request.user)
        serializer = ProcessorUsageSerializer(processor_usages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class VideoTranscriptionAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get("file")

        if not video_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
                temp_video_path = temp_video.name
                for chunk in video_file.chunks():
                    temp_video.write(chunk)

            # Close the file after writing
            temp_video.close()

            # Extract audio and transcribe it
            audio_path = temp_video_path.replace(".mp4", ".mp3")
            os.system(f"ffmpeg -i {temp_video_path} -q:a 0 -map a {audio_path}")
            transcript = transcribe_audio_with_assemblyai(audio_path)

            # Add subtitles to the video
            subtitled_video_path = add_subtitles_to_video(temp_video_path, transcript)

            # Serve the resulting video
            response = FileResponse(open(subtitled_video_path, "rb"), as_attachment=True)
            response["Content-Disposition"] = 'attachment; filename="transcribed_video.mp4"'
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Cleanup temporary files
            for path in [temp_video_path, audio_path]:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except Exception as cleanup_error:
                    print(f"Error cleaning up file {path}: {cleanup_error}")

