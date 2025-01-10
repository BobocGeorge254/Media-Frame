from django.db import models
from django.conf import settings
from django.utils import timezone

class ProcessorType(models.TextChoices):
    TRANSCRIBE = 'transcribe', 'Transcription'
    PITCH_SHIFT = 'pitch_shift', 'Pitch Shifting'
    NOISE_CANCEL = 'noise_cancel', 'Noise Cancellation'
    BASS_BOOST = 'bass_boost', 'Bass Boost'
    SPEECH_IDENTIFIER = 'speech_identifier', 'Speech Identifier'
    SPEED_UP = 'speed_up', 'Speed Up'

class ProcessorUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='processor_usages')
    processor_type = models.CharField(max_length=50, choices=ProcessorType.choices)
    file = models.FileField(upload_to='processor_files/')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.processor_type} at {self.timestamp}"
