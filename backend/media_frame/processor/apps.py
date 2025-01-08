from django.apps import AppConfig
import whisper

class ProcessorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'processor'

    def ready(self):
        from . import transcription
        transcription.model = whisper.load_model("base")
