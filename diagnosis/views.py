from django.shortcuts import render
from rest_framework import generics, permissions
from .models import DiagnosisRequest
from .serializers import DiagnosisResultSerializer
from DRF_AI.permissions import IsOwnerOrReadOnly

class DiagnosisRequestCreateView(generics.ListCreateAPIView):
    queryset = DiagnosisRequest.objects.all()
    serializer_class = DiagnosisResultSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    



class DiagnosisDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiagnosisResultSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = DiagnosisRequest.objects.all()
