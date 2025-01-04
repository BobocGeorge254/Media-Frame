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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class TranscriptionAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transcript = transcribe_audio(audio_file)
            return Response({"transcript": transcript}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@method_decorator(csrf_exempt, name='dispatch')
class PitchShiftingAPIView(APIView):
    parser_classes = [MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        print("Request data:", request.data)
        print("Request files:", request.FILES)
        audio_file = request.FILES.get('file')

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

            # Serve the pitch-shifted audio file as a download
            response = FileResponse(open(new_audio_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="shifted_audio.mp3"'

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@method_decorator(csrf_exempt, name='dispatch')
class NoiseCancelAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Perform noise cancellation
            new_audio_path = noisecancel_audio(audio_file)

            # Serve the noise-canceled audio file as a download
            response = FileResponse(open(new_audio_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="noisecancelled_audio.mp3"'

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@method_decorator(csrf_exempt, name='dispatch')
class BassBoostAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Perform bass boosting
            new_audio_path = bassboost_audio(audio_file)

            # Serve the bass-boosted audio file as a download
            response = FileResponse(open(new_audio_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="bassboosted_audio.mp3"'

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@method_decorator(csrf_exempt, name='dispatch')
class SpeechIdentifierAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Identify speech in the audio file
            speech_info = speechidentifier_audio(audio_file)

            return Response({"speech_info": speech_info}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@method_decorator(csrf_exempt, name='dispatch')
class SpeedUpAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('file')

        if not audio_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the speed factor from the request (default to 1.5 if not provided)
            speed_factor = float(request.data.get('speed_factor', 1.5))

            # Perform speed-up
            new_audio_path = speedup_audio(audio_file, speed_factor)

            # Serve the processed audio file as a download
            response = FileResponse(open(new_audio_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="speedup_audio.mp3"'

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

