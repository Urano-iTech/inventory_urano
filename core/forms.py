from django import forms
from django.db import models
from core.models import *


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = "__all__"


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = "__all__"


class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = "__all__"
