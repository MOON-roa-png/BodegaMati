from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "bodega"

urlpatterns = [
    # LOGIN / LOGOUT
    path("usuarios/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("usuarios/logout/", auth_views.LogoutView.as_view(next_page="bodega:login"), name="logout"),

    # Registro inicial y gestión de usuarios
    path("registro-inicial/", views.registro_inicial, name="registro_inicial"),
    path("usuarios/crear/", views.usuarios_crear, name="usuarios_crear"),

    # HOME / DASHBOARD
    path("", views.dashboard, name="dashboard"),

    # PRODUCTOS
    path("productos/", views.productos, name="productos"),
    path("productos/agregar/", views.agregar_productos, name="agregar_productos"),
    path("productos/editar/<int:pk>/", views.editar_productos, name="editar_productos"),
    path("productos/eliminar/<int:pk>/", views.eliminar_productos, name="eliminar_productos"),

    # PROVEEDORES
    path("proveedores/", views.proveedores_list, name="proveedores"),
    path("proveedores/agregar/", views.proveedores_agregar, name="proveedores_agregar"),
    path("proveedores/editar/<int:pk>/", views.proveedores_editar, name="proveedores_editar"),
    path("proveedores/eliminar/<int:pk>/", views.proveedores_eliminar, name="proveedores_eliminar"),

    # COMPRAS
    path("compras/", views.compras, name="compras"),
    path("compras/editar/<int:pk>/", views.compras_editar, name="compras_editar"),
    path("compras/eliminar/<int:pk>/", views.compras_eliminar, name="compras_eliminar"),

    # VENTAS
    path("ventas/", views.ventas, name="ventas"),
    path("ventas/modificar/<int:index>/", views.ventas_modificar_item, name="ventas_modificar_item"),
    path("ventas/eliminar/<int:index>/", views.ventas_eliminar_item, name="ventas_eliminar_item"),
    path("ventas/vaciar/", views.ventas_vaciar, name="ventas_vaciar"),
    path("ventas/confirmar/", views.confirmar_venta, name="confirmar_venta"),

    # REPORTES
    path("reportes/", views.reportes, name="reportes"),
]
