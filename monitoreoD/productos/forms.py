from django import forms
from .models import Producto
import re

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-z\s]+'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[A-Za-z\s]+'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'costo_estandar': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'costo_promedio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'impuesto_iva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'punto_reorden': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'factor_conversion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or len(nombre.strip()) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        if not re.match(r'^[A-Za-z\s]+$', nombre.strip()):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre.strip()

    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if marca and not re.match(r'^[A-Za-z\s]+$', marca.strip()):
            raise forms.ValidationError("La marca solo puede contener letras y espacios.")
        return marca.strip() if marca else marca

    def clean_costo_estandar(self):
        costo = self.cleaned_data.get('costo_estandar')
        if costo is not None and costo < 0:
            raise forms.ValidationError("El costo no puede ser negativo.")
        return costo

    def clean_precio_venta(self):
        precio = self.cleaned_data.get('precio_venta')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_costo_promedio(self):
        costo = self.cleaned_data.get('costo_promedio')
        if costo is not None and costo < 0:
            raise forms.ValidationError("El costo promedio no puede ser negativo.")
        return costo

    def clean_impuesto_iva(self):
        iva = self.cleaned_data.get('impuesto_iva')
        if iva is not None and (iva < 0 or iva > 100):
            raise forms.ValidationError("El IVA debe estar entre 0 y 100.")
        return iva

    def clean_stock_minimo(self):
        stock = self.cleaned_data.get('stock_minimo')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock mínimo no puede ser negativo.")
        return stock

    def clean_stock_maximo(self):
        stock = self.cleaned_data.get('stock_maximo')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock máximo no puede ser negativo.")
        return stock
