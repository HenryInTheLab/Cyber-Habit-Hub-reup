from django.urls import path

from .apis import ChatbotGenerateApi

urlpatterns = [
    path("chatbot/generate", ChatbotGenerateApi.as_view(), name="chatbot-generate"),
]