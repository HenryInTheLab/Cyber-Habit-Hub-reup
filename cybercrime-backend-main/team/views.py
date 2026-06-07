from django.shortcuts import render
import uuid
from leaderboard.services import award_points
from django.db.models import Sum, F, Q
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from leaderboard.models import Team, TeamMembership, TeamInvite
from .serializers import (
    CreateTeamSerializer, TeamSerializer, TeamInviteSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.
@extend_schema(
    request=CreateTeamSerializer,
    responses={201: TeamSerializer},
    summary="Create a new team",
    description="Create a new team. The authenticated user automatically becomes the captain."
)
class CreateTeamView(APIView):
    """
    Create a new team. The creator automatically becomes captain.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Generate unique invite code
        invite_code = str(uuid.uuid4())

        team = Team.objects.create(
            name=serializer.validated_data["name"],
            invite_code=invite_code,
            created_by=request.user,
            created_at=timezone.now()
        )

        # Add creator as captain
        TeamMembership.objects.create(
            user=request.user,
            team=team,
            role="captain",
            joined_at=timezone.now()
        )

        return Response(TeamSerializer(team).data, status=status.HTTP_201_CREATED)

@extend_schema(
    request=None,
    responses={200: TeamInviteSerializer},
    summary="Generate a team invite",
    description="Generate an invite link for your current team. Invite expires in 7 days."
)
class GenerateTeamInviteView(APIView):
    """
    Generate an invite link for a team (only members).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        membership = TeamMembership.objects.filter(user=request.user).first()
        if not membership:
            return Response({"error": "You are not in a team."}, status=400)

        invite_id = str(uuid.uuid4())
        invite = TeamInvite.objects.create(
            id=invite_id,
            team=membership.team,
            invited_by=request.user,
            created_at=timezone.now(),
            expires_at=timezone.now() + timedelta(days=7),
            is_used=False,
        )

        return Response({
            "invite": TeamInviteSerializer(invite).data,
            "invite_id": invite.id,
            "accept_url": f"/api/teams/invite/{invite.id}/accept/"
        })

@extend_schema(
    request=None,
    responses={200: dict},
    summary="Accept a team invite",
    description="Accept a team invite using its ID and join the corresponding team. A user can only be in one team at a time."
)
class AcceptTeamInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invite_id):
        invite = get_object_or_404(TeamInvite, id=invite_id, is_used=False)

        # Check expiration
        if invite.expires_at and invite.expires_at < timezone.now():
            return Response({"error": "Invite expired."}, status=400)

        # Prevent user from being in multiple teams
        if TeamMembership.objects.filter(user=request.user).exists():
            return Response(
                {"error": "You are already in a team. Leave your current team first."},
                status=400
            )

        # Add user to team
        TeamMembership.objects.create(
            user=request.user,
            team=invite.team,
            role="member",
            joined_at=timezone.now()
        )

        # Mark invite as used
        invite.is_used = True
        invite.save(update_fields=["is_used"])

        # Award inviter points (if inviter exists and is not the same user)
        award_message = None
        if invite.invited_by and invite.invited_by != request.user:
            try:
                stats = award_points(invite.invited_by, "FRIEND_INVITATION")
                award_message = (
                    f"Awarded {stats.points} total points to inviter {invite.invited_by.username}."
                )
            except Exception as e:
                award_message = f"Failed to award inviter points: {str(e)}"

        return Response(
            {
                "message": f"Successfully joined team {invite.team.name}.",
                "inviter_award": award_message
            },
            status=200
        )

                
@extend_schema(
    request=None,
    responses={200: dict},
    summary="Leave current team",
    description="Allows the authenticated user to leave their current team. A user can only be in one team at a time."
)
class LeaveTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        membership = TeamMembership.objects.filter(user=request.user).first()
        if not membership:
            return Response({"error": "You are not in a team."}, status=400)

        team_name = membership.team.name
        membership.delete()

        return Response({"message": f"You have left team {team_name}."})
