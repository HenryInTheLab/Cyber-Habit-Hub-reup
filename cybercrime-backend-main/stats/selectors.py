from typing import Optional
from django.contrib.auth import get_user_model

from common.utils import get_object
from quizzes.models import QuizAttempt
from quizzes.selectors import quiz_module_list
from leaderboard.models import UserStats  # ✅ use UserStats, not Statistic

User = get_user_model()


def stats_get(user_id) -> Optional[UserStats]:
    user = User.objects.get(id=user_id)
    stats, _ = UserStats.objects.get_or_create(user=user)
    return stats


def user_get_challenge_level(user_id: str) -> int:
    stats = get_object(UserStats, user_id=user_id)
    return stats.challenge_level if stats else 1


def user_passed_module(user_id: str, challenge_level: int, module_name: str) -> bool:
    return QuizAttempt.objects.filter(
        user_id=user_id,
        challenge_level=challenge_level,
        module_name=module_name,
        accuracy_pct__gte=80,
        pass_flag=True
    ).exists()


def user_passed_challenge_level(user_id, challenge_level):
    modules = quiz_module_list(challenge_level=challenge_level)
    return all([user_passed_module(user_id, challenge_level, module) for module in modules])
