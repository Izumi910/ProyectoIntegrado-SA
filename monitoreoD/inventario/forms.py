from django import forms
from .models import MovimientoInventario

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['fecha', 'tipo', 'producto', 'proveedor', 'cantidad', 'lote', 'serie', 'fecha_vencimiento', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1', 'placeholder': 'Ej: 10'}),
            'lote': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: L001-2024'}),
            'serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: S123456789'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comentarios sobre el movimiento...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import date
        self.fields['fecha'].label = 'Fecha de Movimiento'
        self.fields['fecha'].initial = date.today()
        self.fields['tipo'].label = 'Tipo de Movimiento'
        self.fields['fecha_vencimiento'].label = 'Fecha de Vencimiento'
        self.fields['proveedor'].required = False
        self.fields['lote'].required = False
        self.fields['serie'].required = False
        self.fields['fecha_vencimiento'].required = False
        self.fields['observaciones'].required = False

    def clean_fecha(self):
        from datetime import date
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha > date.today():
            raise forms.ValidationError("La fecha de movimiento no puede ser futura.")
        return fecha

    def clean_fecha_vencimiento(self):
        from datetime import date
        fecha = self.cleaned_data.get('fecha_vencimiento')
        if fecha and fecha < date.today():
            raise forms.ValidationError("La fecha de vencimiento no puede ser anterior a hoy.")
        return fecha

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0.")
        return int(cantidad) if cantidad == int(cantidad) else cantidad