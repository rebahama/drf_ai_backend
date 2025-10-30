from rest_framework import generics
from .models import DiagnosisResult
from .serializers import DiagnosisResultSerializer
from DRF_AI.permissions import IsOwnerOrReadOnly


class DiagnosisResultDetailView(generics.RetrieveDestroyAPIView):
    queryset = DiagnosisResult.objects.all()
    serializer_class = DiagnosisResultSerializer
    permission_classes = [IsOwnerOrReadOnly]
