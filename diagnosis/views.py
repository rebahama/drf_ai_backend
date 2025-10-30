from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import DiagnosisRequest
from .serializers import DiagnosisRequestSerializer
from diagnosis_result.serializers import DiagnosisResultSerializer as ResultSerializer
from diagnosis_result.models import DiagnosisResult
from DRF_AI.permissions import IsOwnerOrReadOnly  # Make sure you have this custom permission
import google.generativeai as genai
from django.conf import settings

# Configure Gemini API key
genai.configure(api_key=settings.GEMINI_API_KEY)


# List all requests and allow creating a new diagnosis request
class DiagnosisRequestCreateView(generics.ListCreateAPIView):
    queryset = DiagnosisRequest.objects.all()
    serializer_class = DiagnosisRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Save the request with the current user
        diagnosis_request = serializer.save(user=self.request.user)

        # Build prompt for AI
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
            ai_text = response.text if response else "No AI response"
        except Exception as e:
            ai_text = f"Error generating AI result: {str(e)}"

        # Save AI result in the diagnosis_result app
        DiagnosisResult.objects.create(
            request=diagnosis_request,
            result=ai_text
        )
        return diagnosis_request

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        # Return the AI result in the response
        result = DiagnosisResult.objects.get(request=instance)
        return Response(ResultSerializer(result).data, status=status.HTTP_201_CREATED)


# Retrieve / Delete / Update a single diagnosis request
class DiagnosisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiagnosisRequest.objects.all()
    serializer_class = DiagnosisRequestSerializer
    permission_classes = [IsOwnerOrReadOnly]