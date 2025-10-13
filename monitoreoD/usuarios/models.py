from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=30, blank=True, null=True)
    estado = models.CharField(max_length=20, default="ACTIVO")
    mfa_habilitado = models.BooleanField(default=False)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

