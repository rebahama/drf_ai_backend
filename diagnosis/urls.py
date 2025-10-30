from django.urls import path
from .views import DiagnosisRequestCreateView

urlpatterns = [
    path('diagnose/', DiagnosisRequestCreateView.as_view(), name='diagnose'),
]