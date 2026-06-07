from rest_framework import serializers


class ChatbotInputSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=2048)

class ChatbotOutputSerializer(serializers.Serializer):
    response = serializers.CharField()
    follow_up_questions = serializers.ListField(
        child=serializers.CharField(), required=False
    )