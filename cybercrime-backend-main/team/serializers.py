from rest_framework import serializers
from leaderboard.models import UserStats, Team, TeamMembership, TeamInvite

class CreateTeamSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "invite_code", "created_by", "created_at"]


class TeamMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = TeamMembership
        fields = ["id", "username", "role", "joined_at"]


class TeamInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvite
        fields = ["id", "team", "invited_by", "created_at", "expires_at", "is_used"]
