from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication

class ExpiringTokenAuthentication(TokenAuthentication):

    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        return timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            # user = token.user
            token.delete()
            # token = self.get_model().objects.create(user=user)
        return is_expire

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.select_related('user').get(key=key)
        except self.get_model().DoesNotExist:
            return (None, None, 'Token inválido')

        if not token.user.is_active:
            return (None, None, 'Usuario inactivo')

        is_expired = self.token_expire_handler(token)

        if is_expired:
            return (None, None, 'Token ha expirado')

        return (token.user, token, None)