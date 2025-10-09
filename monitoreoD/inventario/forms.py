from django import forms
from .models import MovimientoInventario

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'