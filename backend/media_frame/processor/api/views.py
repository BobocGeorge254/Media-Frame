from django.http import FileResponse
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
from authentication.models import CustomUser
from rest_framework import permissions
from processor.models import ProcessorUsage
from django.utils import timezone
from .serializer import ProcessorUsageSerializer

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
