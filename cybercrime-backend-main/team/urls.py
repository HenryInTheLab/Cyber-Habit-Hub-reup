from django.urls import path
from .views import (
    CreateTeamView,
    GenerateTeamInviteView,
    AcceptTeamInviteView,
    LeaveTeamView,
)

urlpatterns = [
    path("create/", CreateTeamView.as_view(), name="create-team"),
    path("invite/", GenerateTeamInviteView.as_view(), name="generate-team-invite"),
    path("invite/<str:invite_id>/accept/", AcceptTeamInviteView.as_view(), name="accept-team-invite"),
    path("leave/", LeaveTeamView.as_view(), name="leave-team"),

]
