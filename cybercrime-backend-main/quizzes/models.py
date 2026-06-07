from django.db import models


class QuizQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    module_name = models.CharField(max_length=200, null=True, blank=True)
    challenge_level = models.IntegerField(null=True, blank=True)
    question_text = models.TextField(null=True, blank=True)
    option_a = models.TextField(null=True, blank=True)
    option_b = models.TextField(null=True, blank=True)
    option_c = models.TextField(null=True, blank=True)
    option_d = models.TextField(null=True, blank=True)
    option_e = models.TextField(null=True, blank=True)
    correct_answer = models.CharField(max_length=10, null=True, blank=True)
    explanation = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'quiz_new'
        managed = False

    @property
    def options(self):
        option_fields = [
            ('option_a', 'A'),
            ('option_b', 'B'),
            ('option_c', 'C'),
            ('option_d', 'D'),
            ('option_e', 'E'),
        ]
        options = []
        for field, letter in option_fields:
            text = getattr(self, field)
            if text not in [None, ""]:
                is_correct = (self.correct_answer == letter)
                options.append({'identifier': letter,'text': text, 'is_answer': is_correct})
        return options

class QuizAttempt(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=36)
    total_questions = models.IntegerField()
    correct_count = models.IntegerField(default=0)
    accuracy_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    module_name = models.CharField(max_length=200, null=True, blank=True)
    challenge_level = models.IntegerField(null=True, blank=True)
    pass_flag = models.BooleanField(default=False)
    feedback_summary = models.TextField(null=True, blank=True)
    feedback_action_items = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'quiz_attempts'
        managed = False

class QuizQuestionAttempt(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=36)
    question_id = models.BigIntegerField()
    chosen_answer = models.CharField(max_length=10)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(null=True, blank=True)
    attempt_id = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'answers_new'
        managed = False