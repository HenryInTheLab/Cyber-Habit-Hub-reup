from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .apis import (UserDetailApi, UserRecoveryApi, UserSignInApi,
                   UserSignUpApi, UserVerifyApi)

urlpatterns = [
    path('me/', UserDetailApi.as_view(), name='detail'),
    path('verify/', UserVerifyApi.as_view(), name='verify'),
    path('signup/', UserSignUpApi.as_view(), name='signup'),
    path('signin/', UserSignInApi.as_view(), name='signin'),
    path('recover/', UserRecoveryApi.as_view(), name='recover'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
