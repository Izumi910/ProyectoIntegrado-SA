from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
import re

class UsuarioCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez'}))
    
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'rol', 'estado', 'mfa_habilitado', 'area', 'observaciones']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: jperez'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: juan.perez@empresa.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +56912345678'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ventas, Administración, Bodega'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comentarios adicionales sobre el usuario...'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'mfa_habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'autocomplete': 'off', 
            'class': 'form-control', 
            'placeholder': 'Mínimo 8 caracteres'
        })
        self.fields['password2'].widget.attrs.update({
            'autocomplete': 'off', 
            'class': 'form-control', 
            'placeholder': 'Confirma la contraseña'
        })
        self.fields['estado'].choices = [('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')]
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['telefono'].label = 'Teléfono'
        self.fields['mfa_habilitado'].label = 'Autenticación de dos factores'

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
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'rol', 'estado', 'mfa_habilitado', 'area', 'observaciones']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: jperez'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: juan.perez@empresa.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +56912345678'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ventas, Administración, Bodega'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comentarios adicionales...'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'mfa_habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
        self.fields['estado'].choices = [('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')]
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['telefono'].label = 'Teléfono'
        self.fields['mfa_habilitado'].label = 'Autenticación de dos factores'

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

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: juan.perez@empresa.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +56912345678'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['telefono'].label = 'Teléfono'
        self.fields['avatar'].label = 'Foto de Perfil'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'content_type'):
            if avatar.size > 2 * 1024 * 1024:  # 2MB
                raise ValidationError('La imagen no puede superar los 2MB.')
            if not avatar.content_type.startswith('image/'):
                raise ValidationError('El archivo debe ser una imagen.')
        return avatar

class CambiarContrasenaForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'}),
        label='Contraseña Actual'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
        label='Nueva Contraseña'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'}),
        label='Confirmar Nueva Contraseña'
    )

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            if len(password) < 8:
                raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
            if not re.search(r'[A-Z]', password):
                raise ValidationError('La contraseña debe contener al menos una mayúscula.')
            if not re.search(r'[0-9]', password):
                raise ValidationError('La contraseña debe contener al menos un número.')
        return password