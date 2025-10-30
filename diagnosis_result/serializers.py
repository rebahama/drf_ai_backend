from rest_framework import serializers
from .models import DiagnosisResult


class DiagnosisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisResult
        fields = "__all__"
