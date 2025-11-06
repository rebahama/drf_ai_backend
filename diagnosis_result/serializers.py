from rest_framework import serializers
from .models import DiagnosisResult
from django.contrib.humanize.templatetags.humanize import naturaltime


class DiagnosisResultSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    request_info = serializers.SerializerMethodField()
    original_prompt = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='request.user.username')
    user = serializers.ReadOnlyField(source='request.user.id')
    car_model = serializers.ReadOnlyField(source='request.car_model')
    car_make = serializers.ReadOnlyField(source='request.car_make')

    class Meta:
        model = DiagnosisResult
        fields = [
            'id',
            'original_prompt',
            'car_model',
            'car_make',
            'owner',
            'user',
            'result',
            'request',
            'request_info',
            'created_at',
        ]

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_request_info(self, obj):
        """Return a simple string showing car info from related request"""
        if obj.request:
            return f"{obj.request.car_make} {obj.request.car_model} ({obj.request.car_year})"
        return None

    def get_original_prompt(self, obj):
        return obj.request.problem_description
