"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from validate.apis import UrlValidateApi

urlpatterns = [
    path('', RedirectView.as_view(url='/api/schema/docs/', permanent=False)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/', SpectacularSwaggerView.as_view(), name='docs'),
    path('users/', include('users.urls'), name='users'),  
    path('validate/', UrlValidateApi.as_view(), name='validate'),
    path('quizzes/', include('quizzes.urls'), name='quizzes'),
    path('videos/', include("videos.urls")),
    path('infographics/', include('infographic.urls')),
    path('ai/', include('ai.urls')),  
    path('articles/', include('articles.urls')),  
    path('stats/', include('stats.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    path('team/', include('team.urls')),
]
