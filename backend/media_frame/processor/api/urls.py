from django.urls import path
from .views import TranscriptionAPIView, PitchShiftingAPIView, NoiseCancelAPIView, BassBoostAPIView, SpeechIdentifierAPIView, SpeedUpAPIView, ProcessorUsageAPIView

urlpatterns = [
    path('transcribe/', TranscriptionAPIView.as_view() , name='transcribe'),
    path('shift/', PitchShiftingAPIView.as_view(), name='shift'),
    path('noisecancel/', NoiseCancelAPIView.as_view(), name='noisecancel'),
    path('bassboost/', BassBoostAPIView.as_view(), name='bassboost'),
    path('speechidentifier/', SpeechIdentifierAPIView.as_view(), name='speechidentifier'),
    path('speedup/', SpeedUpAPIView.as_view(), name='speedup'),
    path('processor-usage/', ProcessorUsageAPIView.as_view(), name='processor-usage') 

]