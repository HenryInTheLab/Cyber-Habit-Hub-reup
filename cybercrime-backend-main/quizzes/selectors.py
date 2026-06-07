from typing import Optional

from django.db.models.query import QuerySet

from common.utils import get_object
from quizzes.filters import QuizFilter
from quizzes.models import QuizAttempt, QuizQuestion, QuizQuestionAttempt


def quiz_get(id) -> Optional[QuizQuestion]:
    return get_object(QuizQuestion, id=id)

def quiz_list(*, filters=None) -> QuerySet[QuizQuestion]:
    filters = filters or {}
    qs = QuizQuestion.objects.all()
    return QuizFilter(filters, qs).qs

def quiz_list_random(*, filters=None, count) -> QuerySet[QuizQuestion]:
    qs = quiz_list(filters=filters)
    return qs.order_by('?')[:count]

def quiz_module_list(challenge_level: Optional[int] = None) -> list[str]:
    qs = QuizQuestion.objects.all()
    if challenge_level is not None:
        qs = qs.filter(challenge_level=challenge_level)
    return list(
        qs.exclude(module_name__isnull=True)
          .exclude(module_name__exact="")
          .values_list('module_name', flat=True)
          .distinct()
    )

def quiz_attempt_get(id) -> Optional[QuizAttempt]:
    return get_object(QuizAttempt, id=id)

def quiz_attempts_get_by_user(user_id) -> QuerySet[QuizAttempt]:
    return QuizAttempt.objects.filter(user_id=user_id)

def quiz_question_attempt_get(id) -> Optional[QuizQuestionAttempt]:
    return get_object(QuizQuestionAttempt, id=id)

def quiz_question_attempt_get_by_user_question_attempt(user_id, question_id, attempt_id) -> Optional[QuizQuestionAttempt]:
    return get_object(
        QuizQuestionAttempt,
        user_id=user_id,
        question_id=question_id,
        attempt_id=attempt_id
    )

def quiz_question_attempts_get_by_user_attempt(user_id, attempt_id) -> QuerySet[QuizQuestionAttempt]:
    return QuizQuestionAttempt.objects.filter(
        user_id=user_id,
        attempt_id=attempt_id
    )