from rest_framework import generics, permissions, status, filters
from django.db.models import Count
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import DiagnosisRequest
from .serializers import DiagnosisRequestSerializer
from diagnosis_result.serializers import DiagnosisResultSerializer as ResultSerializer
from diagnosis_result.models import DiagnosisResult
from DRF_AI.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


genai.configure(api_key=settings.GEMINI_API_KEY)


class DiagnosisRequestCreateView(generics.ListCreateAPIView):
    queryset = DiagnosisRequest.objects.annotate(
        posts_count=Count('user__diagnosisrequest')
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'car_make',
        'car_model'
    ]

    serializer_class = DiagnosisRequestSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        diagnosis_request = serializer.save(user=self.request.user)

        prompt = f"""
            You are an expert automotive mechanic with decades of experience diagnosing and repairing cars.
            You have in-depth knowledge of common and rare issues for all car makes, models, and years.
            Your instructions are extremely practical, and DIY-friendly
            for someone with basic to intermediate mechanical skills.

            Important rule: You will only answer car-related questions.
            If the question is not about a car or vehicle,
            politely refuse and explain
            that you can only provide automotive advice.

            Car Make: {diagnosis_request.car_make}
            Model: {diagnosis_request.car_model}
            Year: {diagnosis_request.car_year}
            Problem: {diagnosis_request.problem_description}

            Please provide:

            1. A clear **step-by-step diagnostic procedure** to identify the root cause of the problem.
            2. **Common causes** for this issue and how to differentiate between them.
            3. **Recommended repairs**, including tools required,
            estimated difficulty, and cost range.
            4. Safety tips and precautions while performing repairs.
            5. Optional DIY tips for cost-effective solutions where possible.

            Present the answer in a structured,
            easy-to-follow format with headings,
            bullet points, and numbered steps. Avoid vague advice; be precise and practical.
            """

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            ai_text = response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            ai_text = f"Error generating AI result: {str(e)}"

        DiagnosisResult.objects.create(
            request=diagnosis_request,
            result=ai_text
        )
        return diagnosis_request

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        result = DiagnosisResult.objects.get(request=instance)
        return Response(ResultSerializer(result).data, status=status.HTTP_201_CREATED)


class DiagnosisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiagnosisRequest.objects.all()
    serializer_class = DiagnosisRequestSerializer
    permission_classes = [IsAdminOrReadOnly]
