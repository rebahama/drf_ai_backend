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
    serializer_class = DiagnosisResultSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DiagnosisResultDetailView(generics.RetrieveDestroyAPIView):
    queryset = DiagnosisResult.objects.all()
    serializer_class = DiagnosisResultSerializer
    permission_classes = [IsOwnerOrReadOnly]
