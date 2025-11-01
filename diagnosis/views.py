from rest_framework import generics, permissions, status, filters
from django.db.models import Count
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import DiagnosisRequest
from .serializers import DiagnosisRequestSerializer
from diagnosis_result.serializers import DiagnosisResultSerializer as ResultSerializer
from diagnosis_result.models import DiagnosisResult
from DRF_AI.permissions import IsOwnerOrReadOnly
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        diagnosis_request = serializer.save(user=self.request.user)

        prompt = f"""
        Car Make: {diagnosis_request.car_make}
        Model: {diagnosis_request.car_model}
        Year: {diagnosis_request.car_year}
        Problem: {diagnosis_request.problem_description}
        Generate step-by-step repair instructions, common causes, and estimated costs.
        """

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            ai_text = response.text if hasattr(response, "text") else str(response)
            logger.info(f"✅ Gemini response: {ai_text[:200]}...")  # logs first 200 chars
        except Exception as e:
            ai_text = f"Error generating AI result: {str(e)}"
            logger.error(f"❌ Gemini error: {e}", exc_info=True)
            print(f"❌ Gemini error: {e}")  # visible in Heroku logs too

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
    permission_classes = [IsOwnerOrReadOnly]
