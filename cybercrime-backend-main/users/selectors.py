from typing import Optional

from common.utils import get_object
from users.models import User


def user_get(id) -> Optional[User]:
    """
    Retrieve a user by their id.
    """
    return get_object(User, id=id)

def user_get_by_username(username: str) -> Optional[User]:
    """
    Retrieve a user by their username.
    """
    return get_object(User, username=username)

def username_exists(username: str) -> bool:
    """
    Check if a username already exists in the database.
    """
    return User.objects.filter(username=username).exists()