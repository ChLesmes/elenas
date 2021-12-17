from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.general_views import UserViewSet, TaskViewSet
from .views.auth_view import Login, Logout

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
]

urlpatterns += router.urls