from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidUserException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The username or 6-digit code is invalid."
    default_code = "invalid_user"
    
class InvalidUserRecoveryException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The username or recovery phrase is invalid."
    default_code = "invalid_user_recovery"