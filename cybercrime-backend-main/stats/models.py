# stats/models.py
from leaderboard.models import UserStats

# Keep backward compatibility
Statistic = UserStats

__all__ = ["Statistic"]
