from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import os


class APIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication class that checks for API key in headers.
    """
    
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            raise AuthenticationFailed('API key is required')
        
        expected_key = os.getenv('API_KEY', 'default-secret-key')
        
        if api_key != expected_key:
            raise AuthenticationFailed('Invalid API key')
        
        # Return None as user (we're not using Django's user model)
        return (None, None)
