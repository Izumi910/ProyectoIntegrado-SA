from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    rol = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, default="ACTIVO")
    mfa_habilitado = models.BooleanField(default=False)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
