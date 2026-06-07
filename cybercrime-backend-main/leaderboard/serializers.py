from rest_framework import serializers
from .models import UserStats, Team, TeamMembership, TeamInvite, PrivacySetting


# ---------------- Existing ---------------- #
class UserRowSerializer(serializers.Serializer):
    username = serializers.CharField()
    points = serializers.IntegerField()
    challenge_level = serializers.IntegerField()
    badge = serializers.CharField(allow_null=True)


class TeamRowSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    team = serializers.CharField()
    points = serializers.IntegerField()
    
    
class PrivacySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacySetting
        fields = [
            "show_score",
            "show_level",
            "show_badges",
            "show_achievements",
            "allow_public_ranking",
        ]