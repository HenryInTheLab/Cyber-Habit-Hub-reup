# leaderboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ---------- Public Leaderboards ----------
    path("global/", views.global_leaderboard, name="global-leaderboard-public"),
    path("team/<int:team_id>/", views.team_leaderboard, name="team-leaderboard"),
    path("teams/", views.global_team_leaderboard, name="global-team-leaderboard"),

    # ---------- Authenticated Leaderboards ----------
    path("global/auth/", views.GlobalLeaderboardView.as_view(), name="global-leaderboard-auth"),
    path("my-team/", views.MyTeamLeaderboardView.as_view(), name="my-team-leaderboard"),
    path("me/", views.MyStatsView.as_view(), name="my-stats"),

    # ---------- User Activity ----------
    path("activity/", views.my_activity_log, name="my-activity-log"),

    # ---------- Privacy Settings ----------
    path("privacy/", views.MyPrivacySettingView.as_view(), name="my-privacy-setting"),
]
