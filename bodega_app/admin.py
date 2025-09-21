from django.contrib import admin
from .models import Usuario, Proveedor, Producto, Venta, DetalleVenta, Compra

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "rol", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "contacto")
    search_fields = ("nombre",)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "proveedor", "precio_compra", "precio_venta", "stock", "stock_minimo")
    search_fields = ("nombre",)

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "tipo", "total")
    date_hierarchy = "fecha"
    inlines = [DetalleVentaInline]

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "producto", "cantidad", "precio_total", "proveedor")
    date_hierarchy = "fecha"
