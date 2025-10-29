from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import re

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'estado', 'mfa_habilitado', 'area', 'observaciones']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-z\\s]+'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono is not None:
            if telefono < 0:
                raise forms.ValidationError("El teléfono no puede ser negativo.")
        return telefono

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area and not re.match(r'^[A-Za-z\\s]+$', area.strip()):
            raise forms.ValidationError("El área solo puede contener letras y espacios.")
        return area.strip() if area else area

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'estado', 'mfa_habilitado', 'area', 'observaciones']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-z\\s]+'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono is not None:
            if telefono < 0:
                raise forms.ValidationError("El teléfono no puede ser negativo.")
        return telefono

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area and not re.match(r'^[A-Za-z\\s]+$', area.strip()):
            raise forms.ValidationError("El área solo puede contener letras y espacios.")
        return area.strip() if area else area