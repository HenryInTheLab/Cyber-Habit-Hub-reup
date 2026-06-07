from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import UrlValidateService


class UrlValidateApi(APIView):
    class UrlValidateInputSerializer(serializers.Serializer):
        url = serializers.URLField()

    class UrlValidateOutputSerializer(serializers.Serializer):
        url = serializers.URLField()
        is_safe = serializers.BooleanField()
        risk_level = serializers.CharField()
        analysis = serializers.CharField()
        suspicious_patterns = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)
        details = serializers.JSONField()
        
    @extend_schema(
        request=UrlValidateInputSerializer,
        responses=UrlValidateOutputSerializer,
        description="Validates a URL against Google Safe Browsing API.",
    )
    def post(self, request):
        serializer = self.UrlValidateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url_validation = UrlValidateService().validate(serializer.validated_data["url"])
        data = self.UrlValidateOutputSerializer(url_validation).data
        return Response(data)
        