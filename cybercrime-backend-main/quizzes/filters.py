import django_filters

from quizzes.models import QuizQuestion


class QuizFilter(django_filters.FilterSet):
    class Meta:
        model = QuizQuestion
        fields = ("module_name", "challenge_level")