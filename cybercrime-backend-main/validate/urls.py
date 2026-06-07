from django.urls import path

from .apis import UrlValidateApi

urlpatterns = [
    path('', UrlValidateApi.as_view(), name='url-validate'),
]