from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='empleado')

    def __str__(self):
        return self.username

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=0)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def en_riesgo(self):
        return self.stock <= self.stock_minimo

class Venta(models.Model):
    TIPO_VENTA = [
        ('minorista', 'Minorista'),
        ('mayorista', 'Mayorista'),
    ]
    total = models.DecimalField(max_digits=12, decimal_places=0, default=Decimal('0'))
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPO_VENTA)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='compras')
    cantidad = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=12, decimal_places=0)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra {self.id} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
