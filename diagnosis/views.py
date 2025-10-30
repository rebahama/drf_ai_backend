from django.shortcuts import render
from rest_framework import generics, permissions
from .models import DiagnosisRequest
from .serializers import DiagnosisResultSerializer

class DiagnosisRequestCreateView(generics.ListCreateAPIView):
    queryset = DiagnosisRequest.objects.all()
    serializer_class = DiagnosisResultSerializer
