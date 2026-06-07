from typing import List

from django.db import transaction

from common.services import model_update
from leaderboard.models import UserStats
from users.models import User


@transaction.atomic
def user_create(
    *, username: str, totp_secret: str, recovery_phrase: str, is_active: bool = True, is_staff: bool = False,
) -> User:
    user = User.objects.create_user(username=username, totp_secret=totp_secret, recovery_phrase=recovery_phrase, is_active=is_active, is_staff=is_staff)
    UserStats.objects.get_or_create(user_id=user.id)
    return user

@transaction.atomic
def user_update(*, user: User, data) -> User:
    non_side_effect_fields: List[str] = [
        "username",
        "totp_secret",
        "is_active",
        "is_verified"
    ]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    return user