from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import (
    UserStats,
    Team,
    TeamMembership,
    TaskLog,
    PrivacySetting,
)
from .serializers import PrivacySettingSerializer


# ---------- Helpers ----------

def _badge_dict(badge):
    if not badge:
        return None
    return {
        "name": badge.name,
        "description": badge.description,
        "icon_url": badge.icon_path,
    }


def _apply_privacy(user_stats):
    """
    Apply user's privacy settings to leaderboard entry.
    Returns dict or None if user opted out completely.
    """
    privacy = getattr(user_stats.user, "privacy", None)
    if not privacy:
        # fallback: treat as fully public
        return {
            "username": user_stats.user.username,
            "points": int(user_stats.points or 0),
            "challenge_level": int(user_stats.challenge_level or 1),
            "badge": _badge_dict(user_stats.badge),
        }

    if not privacy.allow_public_ranking:
        return None  # excluded entirely

    return {
        "username": user_stats.user.username,
        "points": int(user_stats.points or 0) if privacy.show_score else None,
        "challenge_level": int(user_stats.challenge_level or 1) if privacy.show_level else None,
        "badge": _badge_dict(user_stats.badge) if privacy.show_badges else None,
    }


# ---------- Function-based endpoints ----------

@extend_schema(
    request=None,
    responses={200: list},
    summary="Global leaderboard (public)",
    description="Top 50 users globally, respecting privacy settings."
)
@api_view(["GET"])
def global_leaderboard(request):
    qs = (
        UserStats.objects
        .select_related("user", "badge", "user__privacy")
        .order_by("-points")[:50]
    )
    data = []
    for s in qs:
        safe = _apply_privacy(s)
        if safe:
            data.append(safe)
    return Response(data)


@extend_schema(
    request=None,
    responses={200: dict},
    summary="Team leaderboard (public)",
    description="Leaderboard within a specific team, respecting privacy settings."
)
@api_view(["GET"])
def team_leaderboard(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    members = (
        team.memberships
        .select_related("user__userstats", "user__userstats__badge", "user__privacy")
        .order_by("-user__userstats__points")
    )

    leaderboard = []
    for m in members:
        stats = getattr(m.user, "userstats", None)
        if stats:
            safe = _apply_privacy(stats)
            if safe:
                leaderboard.append(safe)

    team_points = sum(entry["points"] or 0 for entry in leaderboard if entry["points"] is not None)

    return Response({
        "team": {
            "id": team.id,
            "name": team.name,
            "points": team_points,
            "member_count": members.count(),
        },
        "leaderboard": leaderboard,
    })


@extend_schema(
    request=None,
    responses={200: dict},
    summary="My team leaderboard",
    description="Leaderboard for the authenticated user's team, respecting privacy settings."
)
@api_view(["GET"])
def my_team_leaderboard(request):
    membership = (
        TeamMembership.objects
        .select_related("team")
        .filter(user=request.user)
        .first()
    )
    if not membership:
        return Response({"error": "User is not in any team"}, status=404)

    team = membership.team
    members = (
        team.memberships
        .select_related("user__userstats", "user__userstats__badge", "user__privacy")
        .order_by("-user__userstats__points")
    )

    leaderboard = []
    for m in members:
        stats = getattr(m.user, "userstats", None)
        if stats:
            safe = _apply_privacy(stats)
            if safe:
                leaderboard.append(safe)

    return Response({"team": team.name, "leaderboard": leaderboard})


@extend_schema(
    request=None,
    responses={200: list},
    summary="Global team leaderboard",
    description="Teams ranked by sum of members' visible points."
)
@api_view(["GET"])
def global_team_leaderboard(request):
    teams = Team.objects.prefetch_related("memberships__user__userstats", "memberships__user__privacy")

    data = []
    for team in teams:
        leaderboard = []
        for m in team.memberships.all():
            stats = getattr(m.user, "userstats", None)
            if stats:
                safe = _apply_privacy(stats)
                if safe:
                    leaderboard.append(safe)

        team_points = sum(entry["points"] or 0 for entry in leaderboard if entry["points"] is not None)
        data.append({
            "team_id": team.id,
            "team": team.name,
            "points": team_points,
        })

    # sort by points desc
    data = sorted(data, key=lambda t: t["points"], reverse=True)
    return Response(data)


@extend_schema(
    request=None,
    responses={200: list},
    summary="My recent activity log",
)
@api_view(["GET"])
def my_activity_log(request):
    logs = (
        TaskLog.objects
        .filter(user=request.user)
        .select_related("origin")
        .order_by("-completed_at")
    )
    data = [{
        "points": log.points_awarded,
        "reward": log.origin.name if log.origin else None,
        "meta": log.meta_json,
        "completed_at": log.completed_at,
    } for log in logs]
    return Response(data)


# ---------- Class-based endpoints ----------

@extend_schema(
    request=None,
    responses={200: dict},
    summary="Global leaderboard (authenticated)",
    description="Top 50 users globally. Login required."
)
class GlobalLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = (
            UserStats.objects
            .select_related("user", "badge", "user__privacy")
            .order_by("-points")[:50]
        )
        leaderboard = []
        for s in stats:
            safe = _apply_privacy(s)
            if safe:
                leaderboard.append(safe)
        return Response({"leaderboard": leaderboard})


@extend_schema(
    request=None,
    responses={200: dict},
    summary="My team leaderboard (class view)",
    description="Leaderboard for the authenticated user's current team."
)
class MyTeamLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        membership = (
            TeamMembership.objects
            .select_related("team")
            .filter(user=request.user)
            .first()
        )
        if not membership:
            return Response({"error": "You are not in any team."}, status=404)

        team = membership.team
        members = (
            team.memberships
            .select_related("user__userstats", "user__userstats__badge", "user__privacy")
            .order_by("-user__userstats__points")
        )

        leaderboard = []
        for m in members:
            stats = getattr(m.user, "userstats", None)
            if stats:
                safe = _apply_privacy(stats)
                if safe:
                    leaderboard.append(safe)

        team_points = sum(entry["points"] or 0 for entry in leaderboard if entry["points"] is not None)

        return Response({
            "team": {
                "id": team.id,
                "name": team.name,
                "points": team_points,
                "member_count": members.count(),
            },
            "leaderboard": leaderboard,
        })


@extend_schema(
    request=None,
    responses={200: dict},
    summary="Get my stats",
    description="Returns the authenticated user's current stats, ignoring privacy (for self-view)."
)
class MyStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = get_object_or_404(UserStats, user=request.user)
        return Response({
            "username": request.user.username,
            "points": int(stats.points or 0),
            "challenge_level": int(stats.challenge_level or 1),
            "badge": _badge_dict(stats.badge),
        })


# ---------- Privacy Setting Endpoints ----------

@extend_schema(
    summary="View or update my privacy settings",
    description="Retrieve or update your privacy settings (PATCH supports partial updates).",
    request=PrivacySettingSerializer,      # 👈 tell Swagger what request body looks like
    responses={200: PrivacySettingSerializer},
)
class MyPrivacySettingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        setting, _ = PrivacySetting.objects.get_or_create(user=request.user)
        serializer = PrivacySettingSerializer(setting)
        return Response(serializer.data)

    def patch(self, request):
        setting, _ = PrivacySetting.objects.get_or_create(user=request.user)
        serializer = PrivacySettingSerializer(setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
