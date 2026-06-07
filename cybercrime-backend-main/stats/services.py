from leaderboard.models import UserStats
from stats.selectors import user_get_challenge_level, user_passed_challenge_level


def stats_update(stats, data):
    for field, value in data.items():
        setattr(stats, field, value)
    stats.save(update_fields=data.keys())
    return stats


def user_challenge_level_update(user_id: str):
    """
    Update the user's challenge level if they have passed all modules
    in the current level.
    """
    level = user_get_challenge_level(user_id)
    if user_passed_challenge_level(user_id, level):
        stats, _ = UserStats.objects.get_or_create(user_id=user_id)
        if stats.challenge_level < level + 1:
            stats = stats_update(stats, {"challenge_level": level + 1})
            return True
    return False


def points_update(user_id: str, points: float):
    stats, _ = UserStats.objects.get_or_create(user_id=user_id)
    current_points = stats.points if stats.points is not None else 0
    new_points = current_points + points
    stats = stats_update(stats, {"points": new_points})
    return stats
