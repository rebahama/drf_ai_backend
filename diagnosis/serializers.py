from rest_framework import serializers
from .models import DiagnosisRequest
from django.contrib.humanize.templatetags.humanize import naturaltime


class DiagnosisRequestSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    posts_count = serializers.IntegerField(read_only=True)
    is_owner = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = DiagnosisRequest
        fields = [
            'id',
            'user',
            'owner',
            'car_make',
            'car_model',
            'car_year',
            'problem_description',
            'created_at',
            'is_owner',
            'posts_count',
        ]

    def get_is_owner(self, obj):
        """Return True if the logged-in user is the same as obj.user."""
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            return obj.user == request.user
        return False

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)
