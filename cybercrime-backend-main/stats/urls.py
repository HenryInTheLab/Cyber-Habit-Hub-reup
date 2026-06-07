from django.urls import path

from stats.apis import StatsApi

urlpatterns = [
    path('', StatsApi.as_view(), name='stats'),
]