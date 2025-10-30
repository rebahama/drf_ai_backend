from django.db import models
from django.contrib.auth.models import User

class DiagnosisRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField(null=True, blank=True)
    problem_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_make} {self.car_model} ({self.car_year}) - {self.id}"