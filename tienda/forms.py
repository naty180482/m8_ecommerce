from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Producto


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese su usuario"})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Ingrese su contraseña"})
    )


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["categoria", "nombre", "descripcion", "precio", "stock", "imagen", "activo", "destacado"]
        widgets = {
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "destacado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock