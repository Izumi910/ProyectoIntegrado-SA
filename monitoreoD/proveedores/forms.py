from django import forms
from .models import Proveedor, ProveedorProducto
import re

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        exclude = ['estado']
        widgets = {
            'rut_nif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Distribuidora ABC S.A.'}),
            'nombre_fantasia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ABC Distribuciones'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: contacto@proveedor.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +56912345678'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.proveedor.com'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Av. Principal 123, Oficina 45'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Santiago, Valparaíso'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Chile'}),
            'condiciones_pago': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 30 días, Contado, 15 días'}),
            'moneda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: CLP, USD, EUR'}),
            'contacto_principal_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: María González'}),
            'contacto_principal_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: maria@proveedor.com'}),
            'contacto_principal_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +56987654321'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comentarios adicionales sobre el proveedor...'}),
        }

    def clean_rut_nif(self):
        rut = self.cleaned_data.get('rut_nif')
        if not rut:
            raise forms.ValidationError("El RUT/NIF es requerido.")
        try:
            if self.instance.pk:
                if Proveedor.objects.filter(rut_nif=rut).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError("Este RUT ya está registrado.")
            else:
                if Proveedor.objects.filter(rut_nif=rut).exists():
                    raise forms.ValidationError("Este RUT ya está registrado.")
        except Exception:
            raise forms.ValidationError("Error al validar el RUT.")
        return rut

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rut_nif'].label = 'RUT/NIF'
        self.fields['razon_social'].label = 'Razón Social'
        self.fields['nombre_fantasia'].label = 'Nombre de Fantasía'
        self.fields['sitio_web'].label = 'Sitio Web'
        self.fields['direccion'].label = 'Dirección'
        self.fields['condiciones_pago'].label = 'Condiciones de Pago'
        self.fields['contacto_principal_nombre'].label = 'Nombre del Contacto'
        self.fields['contacto_principal_email'].label = 'Email del Contacto'
        self.fields['contacto_principal_telefono'].label = 'Teléfono del Contacto'

    def clean_razon_social(self):
        razon_social = self.cleaned_data.get('razon_social')
        if not razon_social or len(razon_social.strip()) < 2:
            raise forms.ValidationError("La razón social debe tener al menos 2 caracteres.")
        return razon_social.strip()

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            try:
                telefono_num = int(telefono.replace('+', '').replace('-', '').replace(' ', ''))
                if telefono_num < 0:
                    raise forms.ValidationError("El teléfono no puede ser negativo.")
            except (ValueError, AttributeError):
                raise forms.ValidationError("Formato de teléfono inválido.")
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
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tiempo_entrega': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio
    
    def clean_tiempo_entrega(self):
        tiempo = self.cleaned_data.get('tiempo_entrega')
        if tiempo is not None and tiempo < 0:
            raise forms.ValidationError("El tiempo de entrega no puede ser negativo.")
        return tiempo