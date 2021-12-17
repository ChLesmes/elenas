from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from tasks_app.authentication_mixins import Authentication, AuthenticationSuperuser
from tasks_app.models import Task
from ..serializers import TaskSerializer, UserSerializer

class UserViewSet(AuthenticationSuperuser, viewsets.ModelViewSet):
    '''
    CRUD de usuarios

    End-point del CRUD de usuarios
    '''
    serializer_class = UserSerializer
    queryset = UserSerializer.Meta.model.objects.all()

class TaskViewSet(Authentication, viewsets.ModelViewSet):
    '''
    CRUD de tareas

    End-point del CRUD de tareas
    '''
    serializer_class = TaskSerializer
    queryset = TaskSerializer.Meta.model.objects.all()

    def list(self, request):
        '''
        End-point no disponible

        No hay permisos para acceder a este end-point
        '''
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        '''
        End-point no disponible

        No hay permisos para acceder a este end-point
        '''
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, user=None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            task = Task(**serializer.validated_data)
            task.user = user
            task.save()
            task_serializer = TaskSerializer(task)
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk = None, user=None):
        task = Task.objects.filter(id=pk, deleted=False).first()
        if task:
            if task.user.id != user.id:
                return Response({'message': 'No tiene permiso'}, status=status.HTTP_401_UNAUTHORIZED)
            task_serializer = TaskSerializer(task, data=request.data)
            if task_serializer.is_valid():
                task_serializer.save()
                return Response(task_serializer.data, status=status.HTTP_200_OK)
            return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Tarea no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, user=None):
        '''
        Elimina virtualmente una tarea

        End-point que elimina virtualmente desde el campo deleted la tarea enviada
        '''
        task = Task.objects.filter(id=pk, deleted=False).first()
        if task:
            if task.user.id != user.id:
                return Response({'message': 'No tiene permiso'}, status=status.HTTP_401_UNAUTHORIZED)
            task.deleted = True
            task.save()
            return Response({'message': 'Tarea eliminada'}, status=status.HTTP_200_OK)
        return Response({'message': 'Tarea no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path='user', url_name='user')
    def users_tasks(self, request, user=None):
        '''
        Obtine las tareas del usaurio

        End-point para obtener las tareas del usuario
        '''

        tasks = Task.objects.filter(user=user.id, deleted=False)

        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(methods=['PUT'], detail=True, url_path='finished', url_name='finished')
    def task_finished(self, request, user=None, pk=None):
        '''
        Cambia el estado de finalización de una tarea

        End-point para cambiar el estado de finalización de una tarea
        '''
        task = Task.objects.filter(id=pk, deleted=False).first()
        
        if task:
            if task.user.id != user.id:
                return Response({'message': 'No tiene permiso'}, status=status.HTTP_401_UNAUTHORIZED)
            task.finished = not task.finished
            task.save()
            task_serializer = self.get_serializer(task)
            return Response(task_serializer.data)
        
        return Response({'message': 'Tarea no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path=r'search/(?P<description>[^/.]+)', url_name='search')
    def task_search(self, request, user=None, description = None):
        '''
        Busca una tarea por su descripción 

        End-point para buscar una tarea por su descripción
        '''
        tasks = Task.objects.filter(user=user.id, description__icontains=description, deleted=False)
        
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)