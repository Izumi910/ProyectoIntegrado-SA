from django import forms
from .models import Proveedor, ProveedorProducto
import re

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-z\s]+'}),
            'rut_nif': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-z\s]+'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-z\s]+'}),
        }

    def clean_rut_nif(self):
        rut = self.cleaned_data['rut_nif']
        if self.instance.pk:
            if Proveedor.objects.filter(rut_nif=rut).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este RUT ya está registrado.")
        else:
            if Proveedor.objects.filter(rut_nif=rut).exists():
                raise forms.ValidationError("Este RUT ya está registrado.")
        return rut

    def clean_razon_social(self):
        razon_social = self.cleaned_data.get('razon_social')
        if razon_social and not re.match(r'^[A-Za-z\s]+$', razon_social.strip()):
            raise forms.ValidationError("La razón social solo puede contener letras y espacios.")
        return razon_social.strip() if razon_social else razon_social

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono is not None and telefono < 0:
            raise forms.ValidationError("El teléfono no puede ser negativo.")
        return telefono

    def clean_ciudad(self):
        ciudad = self.cleaned_data.get('ciudad')
        if ciudad and not re.match(r'^[A-Za-z\s]+$', ciudad.strip()):
            raise forms.ValidationError("La ciudad solo puede contener letras y espacios.")
        return ciudad.strip() if ciudad else ciudad

    def clean_pais(self):
        pais = self.cleaned_data.get('pais')
        if pais and not re.match(r'^[A-Za-z\s]+$', pais.strip()):
            raise forms.ValidationError("El país solo puede contener letras y espacios.")
        return pais.strip() if pais else pais

class ProveedorProductoForm(forms.ModelForm):
    class Meta:
        model = ProveedorProducto
        fields = '__all__'
    