from rest_framework.views import APIView


class BaseApiView(APIView):
    """
    Base API view that standardizes input and output validation using DRF serializers.
    """
    request_serializer_class = None
    response_serializer_class = None
    
    def validate_request(self, request):
        serializer = self.request_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def validate_response(self, response):
        serializer = self.response_serializer_class(data=response)
        serializer.is_valid(raise_exception=True)
        return serializer.data