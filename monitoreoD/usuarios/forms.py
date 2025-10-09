from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombres', 'apellidos', 'telefono', 'rol', 'estado', 'mfa_habilitado', 'area', 'observaciones']
    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombres', 'apellidos', 'telefono', 'rol', 'estado', 'mfa_habilitado', 'area', 'observaciones']
    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email
