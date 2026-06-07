from rest_framework import status
from rest_framework.exceptions import APIException


class QuizAttemptFinalisedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Quiz attempt has been finalised and cannot be updated."
    default_code = "quiz_attempt_finalised"

class QuizChallengeLevelLockedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You have not unlocked this challenge level."
    default_code = "quiz_challenge_level_locked"