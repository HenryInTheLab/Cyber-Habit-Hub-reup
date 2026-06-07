from rest_framework import serializers


class StatsSerializer(serializers.Serializer):
    challenge_level = serializers.IntegerField()
    points = serializers.FloatField()


class UpdatedFieldSerializer(serializers.Serializer):
    field = serializers.CharField()
    value = serializers.CharField()


class StatsUpdateSerializer(serializers.Serializer):
    updated_fields = serializers.ListField(child=UpdatedFieldSerializer(), required=False)
    messages = serializers.ListField(child=serializers.CharField(), required=False)
