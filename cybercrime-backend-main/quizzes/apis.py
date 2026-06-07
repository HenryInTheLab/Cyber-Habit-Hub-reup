from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from quizzes.exceptions import (QuizAttemptFinalisedException,
                                QuizChallengeLevelLockedException)
from quizzes.selectors import (quiz_attempt_get, quiz_attempts_get_by_user,
                               quiz_get, quiz_list, quiz_list_random,
                               quiz_module_list,
                               quiz_question_attempts_get_by_user_attempt)
from quizzes.serializers import (QuizAttemptSerializer,
                                 QuizAttemptUpdateSerializer,
                                 QuizAttemptWithQuestionAndStatsSerializer,
                                 QuizAttemptWithQuestionSerializer,
                                 QuizQuestionAttemptSerializer,
                                 QuizQuestionSerializer)
from quizzes.services import (quiz_attempt_create, quiz_attempt_finalise,
                              quiz_question_attempt_bulk_update)
from quizzes.utils import set_answered_at_for_attempts
from stats.selectors import user_get_challenge_level


class QuizQuestionDetailApi(APIView):

    @extend_schema(
        responses=QuizQuestionSerializer,
        description="Fetches a single quiz question by ID."
    )
    def get(self, request, id):
        quiz = quiz_get(id)
        if quiz is None: raise NotFound()
        serializer = QuizQuestionSerializer(quiz)
        return Response(serializer.data)
    
class QuizQuestionListApi(APIView):
    class QuizQuestionListFilterSerializer(serializers.Serializer):
        module_name = serializers.CharField(max_length=200, required=False)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='module_name', type=str, required=False),
        ],
        responses=QuizQuestionSerializer,
        description="Fetches quiz questions based on optional module filters."
    )
    def get(self, request):
        filters_serializer = self.QuizQuestionListFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        quizzes = quiz_list(filters=filters_serializer.validated_data)
        return Response(QuizQuestionSerializer(quizzes, many=True).data)
    
class QuizAttemptCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    class QuizAttemptCreateFilterSerializer(serializers.Serializer):
        count = serializers.IntegerField(required=False)
        module_name = serializers.CharField(max_length=200, required=False)
        challenge_level = serializers.IntegerField(required=True)
    
    class QuizAttemptCreateOutputSerializer(serializers.Serializer):
        attempt_id = serializers.IntegerField()
        questions = QuizQuestionSerializer(many=True)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='count', type=int, required=False),
            OpenApiParameter(name='module_name', type=str, required=True),
            OpenApiParameter(name='challenge_level', type=int, required=True),
        ],
        responses=QuizAttemptCreateOutputSerializer,
        description="Creates a quiz attempt and returns selected quizzes."
    )
    def post(self, request):
        filters_serializer = self.QuizAttemptCreateFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        if filters_serializer.validated_data.get('challenge_level') > user_get_challenge_level(request.user.id):
            raise QuizChallengeLevelLockedException()
        
        count = filters_serializer.validated_data.get('count', 5)
        filters = {k: v for k, v in filters_serializer.validated_data.items() if k != 'count'}
        quizzes = quiz_list_random(filters=filters, count=count)
        attempt_id, _ = quiz_attempt_create(request.user.id, quizzes, filters_serializer.validated_data.get('module_name', "Mixed"), filters_serializer.validated_data.get('challenge_level'))
        output = {
            "attempt_id": attempt_id,
            "questions": QuizQuestionSerializer(quizzes, many=True).data
        }
        serializer = self.QuizAttemptCreateOutputSerializer(output)
        return Response(serializer.data)

class QuizAttemptUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=QuizAttemptUpdateSerializer,
        responses=QuizAttemptWithQuestionAndStatsSerializer,
        description="Updates fields of an existing quiz attempt."
    )
    def patch(self, request, id):
        serializer = QuizAttemptUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attempt = quiz_attempt_get(id)
        if not attempt: raise NotFound()
        if attempt.finished_at: raise QuizAttemptFinalisedException()
        
        quiz_question_attempts_data = serializer.validated_data['quiz_question_attempts']
        set_answered_at_for_attempts(quiz_question_attempts_data)
        quiz_question_attempt_bulk_update(request.user.id, attempt.id, quiz_question_attempts_data)
        result = quiz_attempt_finalise(request.user.id, attempt) if serializer.validated_data.get('is_final', False) else {
            "attempt": attempt,
            "stats_update": {"updated_fields": [], "messages": []},
        }
        response_data = QuizAttemptWithQuestionAndStatsSerializer(result).data
        return Response(response_data)
    
class QuizAttemptDetailApi(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=QuizAttemptWithQuestionSerializer,
        description="Fetches details for a single quiz attempt by ID."
    )
    def get(self, request, id):
        quiz_attempt = quiz_attempt_get(id)
        if quiz_attempt is None: raise NotFound()
        serializer = QuizAttemptWithQuestionSerializer(quiz_attempt)
        return Response(serializer.data)

class QuizAttemptListApi(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=QuizAttemptSerializer(many=True),
        description="Fetches all quiz attempts for the authenticated user."
    )
    def get(self, request):
        attempts = quiz_attempts_get_by_user(request.user.id)
        serializer = QuizAttemptSerializer(attempts, many=True)
        return Response(serializer.data)
    
class QuizQuestionAttemptListApi(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=QuizQuestionAttemptSerializer(many=True),
        description="Fetches all quiz question attempts for the authenticated user."
    )
    def get(self, request, id):
        quiz_question_attempts = quiz_question_attempts_get_by_user_attempt(request.user.id, id)
        return Response(QuizQuestionAttemptSerializer(quiz_question_attempts, many=True).data)
    
class QuizModuleApi(APIView):
    class QuizModuleFilterSerializer(serializers.Serializer):
        challenge_level = serializers.IntegerField(required=False)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='challenge_level', type=int, required=False),
        ],
        responses=serializers.ListField(),
        description="Fetches all distinct quiz modules."
    )
    def get(self, request):
        filters_serializer = self.QuizModuleFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        challenge_level = filters_serializer.validated_data.get('challenge_level')
        modules = quiz_module_list(challenge_level=challenge_level)
        return Response(modules)
    