from django.urls import path
from .views import DiagnosisResultDetailView

urlpatterns = [
    path('result/<int:pk>/', DiagnosisResultDetailView.as_view(), name='diagnosis-result-detail'),
]
