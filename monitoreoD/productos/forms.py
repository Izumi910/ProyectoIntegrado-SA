from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError("Este campo debe tener al menos 3 caracteres.")
        return nombre
