from django.urls import path
from .views import DiagnosisResultDetailView, DiagnosisResultView

urlpatterns = [
    path('result/', DiagnosisResultView.as_view(), name='diagnosis-result-list'),
    path('result/<int:pk>/', DiagnosisResultDetailView.as_view(), name='diagnosis-result-detail'),
]
