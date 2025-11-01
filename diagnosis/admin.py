# diagnosis/admin.py
from django.contrib import admin
from .models import DiagnosisRequest
from diagnosis_result.models import DiagnosisResult
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

@admin.register(DiagnosisRequest)
class DiagnosisRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_make', 'car_model', 'created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Only generate AI result on creation, not edit
        if not change:
            prompt = f"""
            Car Make: {obj.car_make}
            Model: {obj.car_model}
            Year: {obj.car_year}
            Problem: {obj.problem_description}
            Generate step-by-step repair instructions, common causes, and estimated costs.
            """
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                ai_text = response.text if response else "No AI response"
            except Exception as e:
                ai_text = f"Error generating AI result: {str(e)}"

            DiagnosisResult.objects.create(
                request=obj,
                result=ai_text
            )
