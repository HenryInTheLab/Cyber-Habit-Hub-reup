from decimal import Decimal

from django.forms.models import model_to_dict
from django.utils import timezone

from ai.services import generate_quiz_feedback
from common.services import model_update
from leaderboard.models import RewardPoint
from leaderboard.services import award_points
from quizzes.models import QuizAttempt, QuizQuestionAttempt
from quizzes.selectors import (
    quiz_question_attempt_get_by_user_question_attempt,
    quiz_question_attempts_get_by_user_attempt)
from stats.selectors import User


def get_reward_points(code: str) -> int:
    try:
        return RewardPoint.objects.get(name=code).points_awarded
    except RewardPoint.DoesNotExist:
        return 0


def quiz_attempt_create(user_id, quizzes, module_name, challenge_level):
    attempt = QuizAttempt.objects.create(
        user_id=user_id,
        total_questions=len(quizzes),
        module_name=module_name,
        challenge_level=challenge_level,
    )
    return attempt.id, [
        quiz_question_attempt_create(
            user_id=user_id,
            question_id=quiz.id,
            attempt_id=attempt.id,
        )
        for quiz in quizzes
    ]


def quiz_attempt_update(attempt, data):
    fields = [
        "finished_at",
        "correct_count",
        "accuracy_pct",
        "pass_flag",
        "feedback_summary",
        "feedback_action_items",
    ]
    attempt, _ = model_update(instance=attempt, fields=fields, data=data)
    return attempt


def quiz_attempt_finalise(user_id, attempt):
    quiz_question_attempts = quiz_question_attempts_get_by_user_attempt(user_id, attempt.id)
    correct_count = quiz_question_attempts.filter(is_correct=True).count()
    total_questions = quiz_question_attempts.count()
    accuracy_pct = (
        Decimal(str(round((correct_count / total_questions) * 100, 2)))
        if total_questions
        else Decimal("0.00")
    )

    updated_attempt = quiz_attempt_update(
        attempt,
        {
            "finished_at": timezone.now(),
            "correct_count": correct_count,
            "accuracy_pct": accuracy_pct,
            "pass_flag": accuracy_pct >= 80,
        },
    )
    feedback_obj = generate_quiz_feedback(model_to_dict(updated_attempt))
    summary = getattr(feedback_obj, "summary", None) or getattr(feedback_obj, "text", None)
    action_items = getattr(feedback_obj, "action_items", [])
    updated_attempt = quiz_attempt_update(
        updated_attempt,
        {
            "feedback_summary": summary,
            "feedback_action_items": ",".join(action_items),
        },
    )

    updated_attempt_with_stats_update = {
        "attempt": updated_attempt,
        "stats_update": quiz_points_update(user_id, accuracy_pct),
    }
    return updated_attempt_with_stats_update


def quiz_question_attempt_create(user_id, question_id, attempt_id):
    return QuizQuestionAttempt.objects.create(
        user_id=user_id,
        question_id=question_id,
        attempt_id=attempt_id,
    )


def quiz_question_attempt_update(quiz_question_attempt, data):
    fields = ["chosen_answer", "is_correct", "answered_at"]
    quiz_question_attempt, _ = model_update(
        instance=quiz_question_attempt, fields=fields, data=data
    )
    return quiz_question_attempt


def quiz_question_attempt_bulk_update(user_id, attempt_id, quiz_question_attempts):
    updated_attempts = []
    for quiz_question_attempt in quiz_question_attempts:
        instance = quiz_question_attempt_get_by_user_question_attempt(
            user_id=user_id,
            attempt_id=attempt_id,
            question_id=quiz_question_attempt.get("question_id"),
        )
        if not instance:
            continue
        updated_attempt = quiz_question_attempt_update(instance, quiz_question_attempt)
        updated_attempts.append(updated_attempt)
    return updated_attempts


def quiz_points_update(user_id, accuracy_pct):
    user = User.objects.get(id=user_id)
    if accuracy_pct < 80:
        return {
            "updated_fields": [],
            "messages": ["Module not passed. No points awarded. Please try again."],
        }

    updated_fields, messages = [], []

    if accuracy_pct == 100:
        stats = award_points(user, "TEST_PASS_100")
        messages.append(f"+{get_reward_points('TEST_PASS_100')} points for perfect score!")
    else:
        stats = award_points(user, "TEST_PASS_80")
        messages.append(f"+{get_reward_points('TEST_PASS_80')} points for passing the module.")

    updated_fields.append({"field": "points", "value": stats.points})
    updated_fields.append({"field": "challenge_level", "value": stats.challenge_level})
    if getattr(stats, "badge", None):
        updated_fields.append({"field": "badge", "value": stats.badge.name})
        messages.append(f"New badge earned: {stats.badge.name}!")

    if stats.challenge_level:
        messages.append(f"Current challenge level: {stats.challenge_level}")

    return {"updated_fields": updated_fields, "messages": messages}
