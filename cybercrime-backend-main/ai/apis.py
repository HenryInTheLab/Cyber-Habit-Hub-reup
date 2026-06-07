from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.serializers import ChatbotInputSerializer, ChatbotOutputSerializer
from ai.services import generate_chatbot_response


class ChatbotGenerateApi(APIView):

    @extend_schema(
        request=ChatbotInputSerializer,
        responses=ChatbotOutputSerializer,
        description="Send a prompt to the Gemini chatbot and receive a complete response."
    )
    def post(self, request):
        serializer = ChatbotInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prompt = serializer.validated_data["prompt"]
        try:
            output_serializer = ChatbotOutputSerializer(generate_chatbot_response(prompt))
            return Response(output_serializer.data)
        except Exception as e:
            raise APIException(f"[ERROR] {str(e)}")
