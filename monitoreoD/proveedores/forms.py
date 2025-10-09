from django import forms
from .models import Proveedor, ProveedorProducto

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
    def clean_rut_nif(self):
        rut = self.cleaned_data['rut_nif']
        if Proveedor.objects.filter(rut_nif=rut).exists():
            raise forms.ValidationError("Este RUT ya está registrado.")
        return rut

class ProveedorProductoForm(forms.ModelForm):
    class Meta:
        model = ProveedorProducto
        fields = '__all__'
    