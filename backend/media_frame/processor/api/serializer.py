from rest_framework import serializers
from ..models import ProcessorUsage

class ProcessorUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessorUsage
        fields = ['user', 'processor_type', 'file', 'timestamp']
