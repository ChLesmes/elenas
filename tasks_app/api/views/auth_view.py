from datetime import datetime
from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView

from ..serializers import UserAuthSerializer

class Login(ObtainAuthToken):
    '''
    Login para el api de tasks
    '''

    def post(self, request, *args, **kwargs):

        login_serializer = self.serializer_class(data = request.data, context={'request':request})

        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']

            if not user.is_active:
                return Response({'mensaje': 'Usuario inactivo'}, status.HTTP_401_UNAUTHORIZED)
            
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserAuthSerializer(user)
            
            if created:
                status_code=status.HTTP_201_CREATED
            else:
                status_code=status.HTTP_200_OK

            return Response({
                'token': token.key,
                'user': user_serializer.data,
            }, status=status_code)


        return Response({'mensaje': 'Datos no válidos'}, status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    '''
    Logout para el api de tasks
    '''
    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key=token).first()

            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()

                return Response(status = status.HTTP_200_OK)
            
            return Response({'error':'Datos incorrectos'}, status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error':'Token inválido'}, status.HTTP_400_BAD_REQUEST)

