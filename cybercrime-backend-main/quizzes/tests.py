from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from quizzes import selectors, services


class QuizSelectorsSimpleTestCase(SimpleTestCase):
    @patch("quizzes.selectors.QuizAttempt")
    def test_quiz_attempt_get(self, mock_quiz_attempt):
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_quiz_attempt._default_manager.all.return_value.get.return_value = mock_instance
        result = selectors.quiz_attempt_get(1)
        self.assertEqual(result.id, 1)

    @patch("quizzes.selectors.QuizAttempt")
    def test_quiz_attempts_get_by_user(self, mock_quiz_attempt):
        mock_quiz_attempt.objects.filter.return_value = [MagicMock(id=1), MagicMock(id=2)]
        result = selectors.quiz_attempts_get_by_user(1)
        self.assertEqual(len(result), 2)

class QuizServicesSimpleTestCase(SimpleTestCase):
    @patch("quizzes.services.model_update")
    def test_quiz_attempt_update(self, mock_model_update):
        mock_instance = MagicMock()
        mock_model_update.return_value = (mock_instance, True)
        result = services.quiz_attempt_update(mock_instance, {"finished_at": "now"})
        self.assertEqual(result, mock_instance)

    # @patch("quizzes.services.quiz_question_attempts_get_by_user_attempt")
    # @patch("quizzes.services.quiz_attempt_update")
    # def test_quiz_attempt_finalise(self, mock_quiz_attempt_update, mock_get_by_user_attempt):
    #     mock_attempt = MagicMock(id=1)
    #     mock_qs = MagicMock()
    #     mock_qs.filter.return_value.count.return_value = 2
    #     mock_qs.count.return_value = 4
    #     mock_get_by_user_attempt.return_value = mock_qs
    #     mock_quiz_attempt_update.return_value = mock_attempt
    #     result, _ = services.quiz_attempt_finalise(1, mock_attempt)
    #     self.assertEqual(result, mock_attempt)

    @patch("quizzes.services.QuizQuestionAttempt")
    def test_quiz_question_attempt_create(self, mock_qq_attempt):
        mock_qq_attempt.objects.create.return_value = MagicMock(id=1)
        result = services.quiz_question_attempt_create(1, 2, 3)
        self.assertEqual(result.id, 1)