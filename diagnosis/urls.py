from django.urls import path
from .views import DiagnosisRequestCreateView, DiagnosisDetail

urlpatterns = [
    path('diagnose/', DiagnosisRequestCreateView.as_view(), name='diagnose'),
    path('diagnose/<int:pk>/', DiagnosisDetail.as_view(),)
]
