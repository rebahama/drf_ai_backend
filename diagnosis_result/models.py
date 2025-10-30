from django.db import models
from diagnosis.models import DiagnosisRequest


class DiagnosisResult(models.Model):
    request = models.OneToOneField(
        DiagnosisRequest,
        on_delete=models.CASCADE,
        related_name='result'
    )
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DiagnosisResult for request {self.request.id}"
