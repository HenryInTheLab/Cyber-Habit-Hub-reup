from django.db import transaction
from django.utils import timezone
from django.db.models import F
from .models import UserStats, RewardPoint, TaskLog, Badge
from stats.services import user_challenge_level_update
from videos.models import VideoProgress
from django.shortcuts import get_object_or_404


@transaction.atomic
def award_points(user, reward_code: str):
    """
    Award points to a user based on a RewardPoint code.
    Logs into task_log with proper schema.
    """
    try:
        reward = RewardPoint.objects.get(name=reward_code)
    except RewardPoint.DoesNotExist:
        raise ValueError(f"Invalid reward code: {reward_code}")

    # Insert into task_log with correct columns
    TaskLog.objects.create(
        user=user,                         # ✅ let Django handle FK
        ref_table="system",
        ref_id=None,
        points_awarded=reward.points_awarded,
        completed_at=timezone.now(),
        meta_json={"reward": reward_code}, # ✅ JSONField takes dict directly
        origin=reward,                      
    )

    # Get or create stats
    stats, _ = UserStats.objects.select_for_update().get_or_create(
        user=user,
        defaults={"points": 0, "challenge_level": 1, "updated_at": timezone.now()},
    )

    # Atomic increment
    stats.points = F("points") + reward.points_awarded
    stats.updated_at = timezone.now()
    stats.save(update_fields=["points", "updated_at"])
    stats.refresh_from_db(fields=["points"])

    # Update badge
    new_badge = Badge.objects.filter(requirement__lte=stats.points).order_by("-requirement").first()
    if new_badge and (not stats.badge_id or stats.badge_id != new_badge.id):
        stats.badge_id = new_badge.id
        stats.updated_at = timezone.now()
        stats.save(update_fields=["badge_id", "updated_at"])

    # Update challenge level
    if user_challenge_level_update(user.id):
        stats.refresh_from_db(fields=["challenge_level"])

    return stats

@transaction.atomic
def award_video_completion(user, video):
    """
    Award WATCH_VIDEO reward once when user finishes ≥80% of a video.
    """
    vp = VideoProgress.objects.filter(user_id=user, video_id=video).first()
    if not vp:
        return False

    threshold = video.suggested_reading_time * 60 * 0.8
    if vp.progress < threshold:
        return False

    reward = get_object_or_404(RewardPoint, name="WATCH_VIDEO")

    # 🚫 Prevent duplicate award
    if TaskLog.objects.filter(
        user=user,
        origin=reward,
        ref_table="video",
        ref_id=str(video.id)
    ).exists():
        return False

    # ✅ Create task log
    TaskLog.objects.create(
        user=user,
        origin=reward,
        ref_table="video",
        ref_id=str(video.id),
        points_awarded=reward.points_awarded,
        completed_at=timezone.now(),
        meta_json={
            "reward": reward.name,
            "video_title": video.title,
            "duration": video.suggested_reading_time,
            "event": "video_completed"
        }
    )

    # ✅ Update user stats
    stats, _ = UserStats.objects.select_for_update().get_or_create(
        user=user,
        defaults={"points": 0, "challenge_level": 1, "updated_at": timezone.now()},
    )
    stats.points = F("points") + reward.points_awarded
    stats.updated_at = timezone.now()
    stats.save(update_fields=["points", "updated_at"])
    stats.refresh_from_db(fields=["points"])

    # ✅ Update badge
    new_badge = Badge.objects.filter(requirement__lte=stats.points).order_by("-requirement").first()
    if new_badge and (not stats.badge_id or stats.badge_id != new_badge.id):
        stats.badge_id = new_badge.id
        stats.updated_at = timezone.now()
        stats.save(update_fields=["badge_id", "updated_at"])

    # ✅ Update challenge level
    if user_challenge_level_update(user.id):
        stats.refresh_from_db(fields=["challenge_level"])

    return True


@transaction.atomic
def award_article_click(user, article):
    """
    Award READ_ARTICLE reward once when user clicks an article.
    """
    reward = get_object_or_404(RewardPoint, name="READ_ARTICLE")

    # 🚫 Prevent duplicate award
    if TaskLog.objects.filter(
        user=user,
        origin=reward,
        ref_table="article",
        ref_id=str(article.id)
    ).exists():
        return False

    # ✅ Create task log
    TaskLog.objects.create(
        user=user,
        origin=reward,
        ref_table="article",
        ref_id=str(article.id),
        points_awarded=reward.points_awarded,
        completed_at=timezone.now(),
        meta_json={
            "reward": reward.name,
            "article_title": article.title,
            "author": article.author,
            "event": "article_clicked"
        }
    )

    # ✅ Update user stats
    stats, _ = UserStats.objects.select_for_update().get_or_create(
        user=user,
        defaults={"points": 0, "challenge_level": 1, "updated_at": timezone.now()},
    )
    stats.points = F("points") + reward.points_awarded
    stats.updated_at = timezone.now()
    stats.save(update_fields=["points", "updated_at"])
    stats.refresh_from_db(fields=["points"])

    # ✅ Update badge
    new_badge = Badge.objects.filter(requirement__lte=stats.points).order_by("-requirement").first()
    if new_badge and (not stats.badge_id or stats.badge_id != new_badge.id):
        stats.badge_id = new_badge.id
        stats.updated_at = timezone.now()
        stats.save(update_fields=["badge_id", "updated_at"])

    # ✅ Update challenge level
    if user_challenge_level_update(user.id):
        stats.refresh_from_db(fields=["challenge_level"])

    return True