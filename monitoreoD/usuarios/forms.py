from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'estado', 'mfa_habilitado', 'area', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'off'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'estado', 'mfa_habilitado', 'area', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'autocomplete': 'off'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email
