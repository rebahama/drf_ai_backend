from rest_framework import serializers
from .models import DiagnosisRequest


class DiagnosisRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisRequest
        fields = "__all__"

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
