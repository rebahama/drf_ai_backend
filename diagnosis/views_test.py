from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import google.generativeai as genai
import traceback


@api_view(['GET'])
def test_gemini(request):
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content("Say 'Hello from Gemini if you can read this'")
        return Response({
            "status": "ok",
            "api_key_set": bool(settings.GEMINI_API_KEY),
            "response": response.text
        })
    except Exception as e:
        return Response({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })