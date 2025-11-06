from rest_framework import generics, permissions, filters
from .models import DiagnosisResult
from .serializers import DiagnosisResultSerializer
from django_filters.rest_framework import DjangoFilterBackend
from DRF_AI.permissions import IsOwnerOrReadOnly


class DiagnosisResultView(generics.ListAPIView):
    queryset = DiagnosisResult.objects.all()

    queryset = DiagnosisResult.objects.annotate(
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'request__car_model',
        'request__car_make',
        'request__user__username',
        'request__user__id',
    ]
    search_fields = [
        'result',
        'request__car_make',
        'request__car_model',
        'request__problem_description',
        'request__user__username',
    ]

    serializer_class = DiagnosisResultSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DiagnosisResultDetailView(generics.RetrieveDestroyAPIView):
    queryset = DiagnosisResult.objects.all()
    serializer_class = DiagnosisResultSerializer
    permission_classes = [IsOwnerOrReadOnly]
