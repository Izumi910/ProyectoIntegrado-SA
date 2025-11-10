from django import forms
from .models import Producto
import re

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ['estado']
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: PROD001'}),
            'ean_upc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 7501234567890'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Chocolate con Leche'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción detallada del producto...'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Nestle, Coca Cola'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Classic, Premium'}),
            'uom_compra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: unidad, kg, litro'}),
            'uom_venta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: unidad, kg, litro'}),
            'factor_conversion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': '1.00'}),
            'costo_estandar': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'placeholder': '0'}),
            'costo_promedio': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'placeholder': '0'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0', 'placeholder': '0'}),
            'impuesto_iva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100', 'placeholder': '19.00'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': '10'}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': '100'}),
            'punto_reorden': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': '20'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': '0'}),
            'lote': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: L001-2024'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'dd/mm/aaaa'}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com/imagen.jpg'}),
            'ficha_tecnica_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com/ficha.pdf'}),
            'perishable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'control_por_lote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'control_por_serie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sku'].label = 'Código SKU'
        self.fields['ean_upc'].label = 'Código EAN/UPC'
        self.fields['uom_compra'].label = 'Unidad de compra'
        self.fields['uom_venta'].label = 'Unidad de venta'
        self.fields['factor_conversion'].label = 'Factor de conversión'
        self.fields['costo_estandar'].label = 'Costo estándar'
        self.fields['costo_promedio'].label = 'Costo promedio'
        self.fields['precio_venta'].label = 'Precio de venta'
        self.fields['impuesto_iva'].label = 'IVA (%)'
        self.fields['stock_minimo'].label = 'Stock mínimo'
        self.fields['stock_maximo'].label = 'Stock máximo'
        self.fields['punto_reorden'].label = 'Punto de reorden'
        self.fields['fecha_vencimiento'].label = 'Fecha de vencimiento'
        self.fields['imagen_url'].label = 'URL de imagen'
        self.fields['ficha_tecnica_url'].label = 'URL ficha técnica'
        self.fields['perishable'].label = 'Producto perecedero'
        self.fields['control_por_lote'].label = 'Control por lote'
        self.fields['control_por_serie'].label = 'Control por serie'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or len(nombre.strip()) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
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
    
    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku or len(sku.strip()) < 3:
            raise forms.ValidationError("El SKU debe tener al menos 3 caracteres.")
        return sku.strip().upper()
    
    def clean_factor_conversion(self):
        factor = self.cleaned_data.get('factor_conversion')
        if factor is not None and factor <= 0:
            raise forms.ValidationError("El factor de conversión debe ser mayor a 0.")
        return factor

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
    
    def clean_fecha_vencimiento(self):
        from datetime import date
        fecha = self.cleaned_data.get('fecha_vencimiento')
        if fecha and fecha < date.today():
            raise forms.ValidationError("La fecha de vencimiento no puede ser anterior a hoy.")
        return fecha
