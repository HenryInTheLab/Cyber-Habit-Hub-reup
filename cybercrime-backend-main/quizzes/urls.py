from django.urls import path

from .apis import (QuizAttemptCreateApi, QuizAttemptDetailApi,
                   QuizAttemptListApi, QuizAttemptUpdateApi, QuizModuleApi,
                   QuizQuestionDetailApi, QuizQuestionListApi)

urlpatterns = [
    path('questions/', QuizQuestionListApi.as_view(), name='list'),
    path('questions/<int:id>/', QuizQuestionDetailApi.as_view(), name='detail'),
    path('modules/', QuizModuleApi.as_view(), name='modules'),
    path('attempt/', QuizAttemptCreateApi.as_view(), name='attempt-start'),
    path('attempt/<int:id>', QuizAttemptUpdateApi.as_view(), name='attempt-save'),
    path('attempts/', QuizAttemptListApi.as_view(), name='attempt-get'),
    path('attempts/<int:id>', QuizAttemptDetailApi.as_view(), name='attempt-get'),
]