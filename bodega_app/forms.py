from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, Proveedor, Compra, Usuario


# ----------------------
# Formularios de Usuario
# ----------------------
class RegistroInicialForm(UserCreationForm):
    """
    Form para crear el primer superusuario/admin.
    Solo pide username y password1/password2.
    El campo 'rol' se forzará a 'admin' en el save().
    """
    class Meta:
        model = Usuario
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        user.rol = "admin"
        if commit:
            user.save()
        return user


class UsuarioCrearForm(UserCreationForm):
    """
    Form para que un admin cree usuarios normales o admins.
    Exponemos 'rol' como ChoiceField usando las choices del modelo.
    """
    rol = forms.ChoiceField(choices=Usuario.ROLES, initial="empleado")

    class Meta:
        model = Usuario
        fields = ["username", "rol", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = self.cleaned_data["rol"]
        # Si elige admin, damos permisos básicos de staff (opcional)
        if user.rol == "admin":
            user.is_staff = True
        if commit:
            user.save()
        return user


# ----------------------
# Formularios existentes
# ----------------------
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio_compra', 'precio_venta', 'stock', 'stock_minimo', 'proveedor']

    def clean(self):
        cleaned = super().clean()
        for campo in ('precio_compra', 'precio_venta'):
            if cleaned.get(campo) is not None and cleaned[campo] < 0:
                self.add_error(campo, 'Debe ser un número positivo.')
        for campo in ('stock', 'stock_minimo'):
            if cleaned.get(campo) is not None and cleaned[campo] < 0:
                self.add_error(campo, 'No puede ser negativo.')
        return cleaned


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto']


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['producto', 'cantidad', 'precio_total', 'proveedor']

    def clean_cantidad(self):
        c = self.cleaned_data['cantidad']
        if c <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')
        return c

    def clean_precio_total(self):
        p = self.cleaned_data['precio_total']
        if p <= 0:
            raise forms.ValidationError('El precio total debe ser mayor a 0.')
        return p
