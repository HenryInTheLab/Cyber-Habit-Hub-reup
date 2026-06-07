from rest_framework import serializers

from quizzes.selectors import (quiz_get,
                               quiz_question_attempts_get_by_user_attempt)
from stats.serializers import StatsUpdateSerializer


class QuizQuestionOptionSerializer(serializers.Serializer):
    identifier = serializers.CharField() 
    text = serializers.CharField()        
    is_answer = serializers.BooleanField()

class QuizQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    module_name = serializers.CharField(max_length=200)
    challenge_level = serializers.IntegerField(allow_null=True)
    question_text = serializers.CharField(allow_null=True, allow_blank=True)
    options = serializers.ListField(child=QuizQuestionOptionSerializer())
    explanation = serializers.CharField(allow_null=True, allow_blank=True)

    def get_options(self, obj):
        return obj.options
    
class QuizQuestionAttemptSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	chosen_answer = serializers.CharField(allow_null=True, allow_blank=True)
	is_correct = serializers.BooleanField(allow_null=True)
	answered_at = serializers.DateTimeField(allow_null=True)
	attempt_id = serializers.IntegerField()
	question = QuizQuestionSerializer(required=False)
	
	def to_representation(self, instance):
		data = super().to_representation(instance)
		quiz_obj = quiz_get(instance.question_id)
		data['question'] = QuizQuestionSerializer(quiz_obj).data if quiz_obj else None
		return data

class QuizQuestionAttemptUpdateSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    chosen_answer = serializers.CharField()
    is_correct = serializers.BooleanField()

class QuizAttemptFeedbackSerializer(serializers.Serializer):
    summary = serializers.CharField()
    action_items = serializers.ListField(child=serializers.CharField(), )
    
    def to_representation(self, instance):
        summary = getattr(instance, 'feedback_summary', None)
        action_items_raw = getattr(instance, 'feedback_action_items', None)
        if isinstance(action_items_raw, str):
            action_items = [item.strip() for item in action_items_raw.split(',') if item.strip()]
        else:
            action_items = action_items_raw or []
        return {
            'summary': summary,
            'action_items': action_items
        }

    def to_internal_value(self, data):
        summary = data.get('summary')
        action_items = data.get('action_items', [])
        if isinstance(action_items, list):
            action_items_str = ','.join([str(item).strip() for item in action_items])
        else:
            action_items_str = str(action_items)
        return {
            'feedback_summary': summary,
            'feedback_action_items': action_items_str
        }
        
class QuizAttemptSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    correct_count = serializers.IntegerField()
    accuracy_pct = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    started_at = serializers.DateTimeField()
    finished_at = serializers.DateTimeField(allow_null=True)
    module_name = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    challenge_level = serializers.IntegerField()
    pass_flag = serializers.BooleanField(default=False)
    feedback = QuizAttemptFeedbackSerializer(source="*", required=False, allow_null=True)

class QuizAttemptUpdateSerializer(serializers.Serializer):
    is_final = serializers.BooleanField(required=False, default=False)
    quiz_question_attempts = serializers.ListField(child=QuizQuestionAttemptUpdateSerializer())

class QuizAttemptWithQuestionSerializer(QuizAttemptSerializer):
    quiz_question_attempts = serializers.ListField(child=QuizQuestionAttemptSerializer(), read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        question_attempts = quiz_question_attempts_get_by_user_attempt(instance.user_id, instance.id)
        data['quiz_question_attempts'] = QuizQuestionAttemptSerializer(question_attempts, many=True).data
        return data
    
class QuizAttemptWithQuestionAndStatsSerializer(QuizAttemptWithQuestionSerializer):
    stats_update = StatsUpdateSerializer(required=False)
    
    def to_representation(self, instance):
        # instance is a dict with 'attempt' (model) and 'stats_update' (dict)
        data = super().to_representation(instance['attempt'])
        data['stats_update'] = StatsUpdateSerializer(instance.get('stats_update', {})).data
        return data