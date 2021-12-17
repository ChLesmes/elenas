from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    name=models.CharField(max_length=63, null=False, verbose_name='Título')
    description=models.CharField('Descripción', null=False, max_length=255)
    finished=models.BooleanField(default=False)
    user=models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    deleted=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True) 

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

    def __str__(self) -> str:
        return self.name