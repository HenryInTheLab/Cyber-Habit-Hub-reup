from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    date_joined = serializers.DateTimeField()
    
class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

class UserSignedInSerializer(serializers.Serializer):
    user = UserSerializer()
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()