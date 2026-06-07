import uuid
from django.conf import settings
from django.db import models



class Badge(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    requirement = models.IntegerField()            # points threshold
    description = models.TextField()
    icon_path = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "badge"
        managed = False

    def __str__(self):
        return f"{self.title} ({self.requirement})"


class UserStats(models.Model):
    # Your table uses user_id as the logical PK/unique key
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                db_column="user_id",
                                primary_key=True,
                                related_name="userstats")
    points = models.IntegerField(default=0)
    challenge_level = models.IntegerField(default=1)
    badge = models.ForeignKey(Badge, null=True, blank=True,
                              on_delete=models.SET_NULL, db_column="badge_id")
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "user_stats"
        managed = False

    def __str__(self):
        return f"{self.user_id} → {self.points} pts"


class RewardPoint(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # human name
    points_awarded = models.IntegerField()
    description = models.TextField()

    class Meta:
        db_table = "reward_point"
        managed = False

    def __str__(self):
        return f"{self.code} (+{self.points_awarded})"

class TaskLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="task_logs"
    )
    origin = models.ForeignKey(
        RewardPoint,
        on_delete=models.CASCADE,
        db_column="origin_id",
        null=True, blank=True
    )
    ref_table = models.CharField(max_length=40, null=True, blank=True)
    ref_id = models.CharField(max_length=100, null=True, blank=True)
    points_awarded = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    meta_json = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "task_log"
        managed = False



# --------- Teams (renamed from group) ---------

class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    invite_code = models.CharField(max_length=36, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   db_column="created_by")
    created_at = models.DateTimeField()

    class Meta:
        db_table = "teams"
        managed = False

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             db_column="user_id",
                             related_name="team_memberships")
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
                             db_column="team_id",
                             related_name="memberships")
    role = models.CharField(max_length=20, default="member")  # <— this is why it's missing
    joined_at = models.DateTimeField()

    class Meta:
        db_table = "team_membership"
        managed = False


class TeamInvite(models.Model):
    id = models.CharField(primary_key=True, max_length=36)  # UUID stored as CHAR(36)
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
                             db_column="team_id", related_name="invites")
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   db_column="invited_by")
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = "team_invite"
        managed = False


# --------- Privacy ---------

class PrivacySetting(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                db_column="user_id",
                                related_name="privacy")
    show_score = models.BooleanField(default=True)
    show_level = models.BooleanField(default=True)
    show_badges = models.BooleanField(default=True)
    show_achievements = models.BooleanField(default=True)
    allow_public_ranking = models.BooleanField(default=True)

    class Meta:
        db_table = "privacy_setting"
        managed = False
