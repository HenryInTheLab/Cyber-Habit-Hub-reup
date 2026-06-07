from django.utils import timezone


def set_answered_at_for_attempts(attempts_data):
    for q in attempts_data:
        if (
            q.get('chosen_answer') is not None and
            str(q.get('chosen_answer')).strip() != '' and
            (q.get('answered_at') is None or 'answered_at' not in q)
        ):
            q['answered_at'] = timezone.now()