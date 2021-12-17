from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .authentication import ExpiringTokenAuthentication

class Authentication(object):

    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                return (None, 'Token malformado')
                
            token_expire = ExpiringTokenAuthentication()
            user, token, err = token_expire.authenticate_credentials(token)
            return (user, err)

        return (None, 'Token no enviado')

    def make_response(self, response):
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response
    
    def dispatch(self,request, *args, **kwargs):
        user, err = self.get_user(request)
        if err:
            response = Response({'error': err}, status=status.HTTP_400_BAD_REQUEST)
            return self.make_response(response)
        return super().dispatch(request, user=user, *args, **kwargs)

class AuthenticationSuperuser(object):

    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                return (None, 'Token malformado')
                
            token_expire = ExpiringTokenAuthentication()
            user, token, err = token_expire.authenticate_credentials(token)
            
            return (user, err)

        return (None, 'Token no enviado')

    def make_response(self, response):
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response
    
    def dispatch(self,request, *args, **kwargs):
        user, err = self.get_user(request)
        if err:
            response = Response({'error': err}, status=status.HTTP_400_BAD_REQUEST)
            return self.make_response(response)
        if not user.is_staff or not user.is_superuser:
            response = Response({'error': 'Acceso no autorizado'}, status=status.HTTP_401_UNAUTHORIZED)
            return self.make_response(response)
        return super().dispatch(request, *args, **kwargs)