import factory

from faker import Faker
from django.contrib.auth.models import User
from .models import Task

fake = Faker()

class UserCommonFactory(factory.Factory):
    class Meta:
        model = User

    username = 'paco123'
    first_name = 'Paco el flaco'
    last_name = 'Martinez'
    password = '123456'
    email = 'pacoflaco@gmail.com'
    is_staff = False
    is_superuser = False

class UserAdminFactory(factory.Factory):
    class Meta:
        model = User

    username = 'Raul'
    first_name = 'Raulencio'
    last_name = 'Pataquiva'
    password = '123456'
    email = 'Raulencio@gmail.com'
    is_staff = True
    is_superuser = True

class TaskFactory(factory.Factory):
    class Meta:
        model = Task
    
    name = 'Tarea 1'
    description = 'Descripción de la tarea 1'
    user = factory.SubFactory(UserCommonFactory)