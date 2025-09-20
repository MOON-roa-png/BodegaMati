from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Compra, DetalleVenta, Producto, Proveedor, Venta

Usuario = get_user_model()

# -------------------------
# Helpers carrito (sesión)
# -------------------------
def _get_carrito(request):
    return request.session.setdefault("carrito", [])

def _guardar_carrito(request, carrito):
    request.session["carrito"] = carrito
    request.session.modified = True

# -------------------------
# Helpers de permisos
# -------------------------
def es_admin(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, "rol", "") == "admin")

# -------------------------
# Setup inicial de usuarios
# -------------------------
def registro_inicial(request):
    if Usuario.objects.exists():
        return redirect("bodega:login")

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = (request.POST.get("password") or "").strip()

        if not username or not password:
            messages.error(request, "Usuario y contraseña son obligatorios.")
            return render(request, "registro_inicial.html")

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "Ese nombre de usuario ya existe.")
            return render(request, "registro_inicial.html")

        if len(password) < 4:
            messages.error(request, "La contraseña debe tener al menos 4 caracteres.")
            return render(request, "registro_inicial.html")

        user = Usuario.objects.create_user(username=username, password=password)
        user.rol = "admin"
        user.is_staff = True
        user.is_superuser = True
        user.save()

        messages.success(request, "Administrador creado. Ya puedes iniciar sesión.")
        return redirect("bodega:login")

    return render(request, "registro_inicial.html")

@user_passes_test(es_admin, login_url="/usuarios/login/")
def usuarios_crear(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = (request.POST.get("password") or "").strip()
        rol = (request.POST.get("rol") or "empleado").strip()

        if not username or not password:
            messages.error(request, "Usuario y contraseña son obligatorios.")
            return render(request, "usuarios_crear.html")

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "Ese nombre de usuario ya existe.")
            return render(request, "usuarios_crear.html")

        if rol not in dict(Usuario.ROLES):
            messages.error(request, "Rol inválido.")
            return render(request, "usuarios_crear.html")

        user = Usuario.objects.create_user(username=username, password=password)
        user.rol = rol
        user.is_staff = (rol == "admin")
        user.is_superuser = (rol == "admin")
        user.save()

        messages.success(request, "Usuario creado correctamente.")
        return redirect("bodega:dashboard")

    return render(request, "usuarios_crear.html")

# -------------------------
# Dashboard
# -------------------------
@login_required(login_url="/usuarios/login/")
def dashboard(request):
    total_productos = Producto.objects.count()
    stock_bajo = Producto.objects.filter(stock__lte=F("stock_minimo")).count()
    hoy = timezone.localdate()
    total_ventas_dia = Venta.objects.filter(fecha__date=hoy).aggregate(s=Sum("total"))["s"] or 0
    return render(request, "dashboard.html", {
        "total_productos": total_productos,
        "stock_bajo": stock_bajo,
        "total_ventas_dia": total_ventas_dia,
    })

# -------------------------
# Productos
# -------------------------
@login_required(login_url="/usuarios/login/")
def productos(request):
    qs = Producto.objects.select_related("proveedor").order_by("nombre")
    return render(request, "productos.html", {"productos": qs})

@login_required(login_url="/usuarios/login/")
def agregar_productos(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        precio_compra = request.POST.get("precio_compra", "").strip()
        precio_venta = request.POST.get("precio_venta", "").strip()
        stock = request.POST.get("stock", "").strip()

        if not nombre:
            messages.error(request, "El nombre es obligatorio.")
        elif not precio_compra.isdigit() or not precio_venta.isdigit() or not stock.isdigit():
            messages.error(request, "Precio y stock deben ser números enteros.")
        else:
            Producto.objects.create(
                nombre=nombre,
                precio_compra=int(precio_compra),
                precio_venta=int(precio_venta),
                stock=int(stock),
            )
            messages.success(request, "Producto agregado.")
            return redirect("bodega:productos")

    return render(request, "agregar_productos.html")

agregar_producto = agregar_productos

@login_required(login_url="/usuarios/login/")
def editar_productos(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        precio_compra = request.POST.get("precio_compra", "").strip()
        precio_venta = request.POST.get("precio_venta", "").strip()
        stock = request.POST.get("stock", "").strip()

        if not nombre:
            messages.error(request, "El nombre es obligatorio.")
        elif not precio_compra.isdigit() or not precio_venta.isdigit() or not stock.isdigit():
            messages.error(request, "Precio y stock deben ser números enteros.")
        else:
            producto.nombre = nombre
            producto.precio_compra = int(precio_compra)
            producto.precio_venta = int(precio_venta)
            producto.stock = int(stock)
            producto.save()
            messages.success(request, "Producto actualizado.")
            return redirect("bodega:productos")

    return render(request, "editar_productos.html", {"producto": producto})

@login_required(login_url="/usuarios/login/")
def eliminar_productos(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    messages.info(request, "Producto eliminado.")
    return redirect("bodega:productos")

# -------------------------
# Proveedores
# -------------------------
@login_required(login_url="/usuarios/login/")
def proveedores_list(request):
    if request.method == "POST":
        nombre = (request.POST.get("nombre") or "").strip()
        contacto = (request.POST.get("contacto") or "").strip()
        if not nombre:
            messages.error(request, "El nombre del proveedor es obligatorio.")
        else:
            Proveedor.objects.create(nombre=nombre, contacto=contacto or None)
            messages.success(request, "Proveedor agregado.")
        return redirect("bodega:proveedores")

    proveedores = Proveedor.objects.order_by("nombre")
    return render(request, "proveedores.html", {"proveedores": proveedores})

@login_required(login_url="/usuarios/login/")
def proveedores_agregar(request):
    if request.method != "POST":
        return redirect("bodega:proveedores")

    nombre = (request.POST.get("nombre") or "").strip()
    contacto = (request.POST.get("contacto") or "").strip()
    if not nombre:
        messages.error(request, "El nombre del proveedor es obligatorio.")
    else:
        Proveedor.objects.create(nombre=nombre, contacto=contacto or None)
        messages.success(request, "Proveedor agregado.")
    return redirect("bodega:proveedores")

@login_required(login_url="/usuarios/login/")
def proveedores_editar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method != "POST":
        return redirect("bodega:proveedores")

    nombre = (request.POST.get("nombre") or "").strip()
    contacto = (request.POST.get("contacto") or "").strip()
    if not nombre:
        messages.error(request, "El nombre del proveedor es obligatorio.")
    else:
        proveedor.nombre = nombre
        proveedor.contacto = contacto or None
        proveedor.save(update_fields=["nombre", "contacto"])
        messages.success(request, "Proveedor actualizado.")
    return redirect("bodega:proveedores")

@login_required(login_url="/usuarios/login/")
def proveedores_eliminar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()
    messages.info(request, "Proveedor eliminado.")
    return redirect("bodega:proveedores")

# -------------------------
# Compras
# -------------------------
@login_required(login_url="/usuarios/login/")
def compras(request):
    productos = Producto.objects.order_by("nombre")
    proveedores = Proveedor.objects.order_by("nombre")

    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        nombre_nuevo = request.POST.get("nombre", "").strip()
        precio_compra = request.POST.get("precio_compra", "").strip()
        cantidad = request.POST.get("cantidad", "").strip()
        proveedor_id = request.POST.get("proveedor_id")

        if not cantidad.isdigit() or not precio_compra.isdigit():
            messages.error(request, "Cantidad y precio deben ser enteros.")
            return redirect("bodega:compras")

        cantidad = int(cantidad)
        precio_compra = int(precio_compra)
        if cantidad <= 0 or precio_compra < 0:
            messages.error(request, "Valores inválidos.")
            return redirect("bodega:compras")

        if producto_id:
            prod = get_object_or_404(Producto, pk=producto_id)
        else:
            if not nombre_nuevo:
                messages.error(request, "Nombre del nuevo producto requerido.")
                return redirect("bodega:compras")
            prod = Producto.objects.create(
                nombre=nombre_nuevo,
                precio_compra=precio_compra,
                precio_venta=precio_compra,
                stock=0,
            )

        prod.stock = F("stock") + cantidad
        prod.precio_compra = precio_compra
        prod.save(update_fields=["stock", "precio_compra"])
        prod.refresh_from_db()

        proveedor = get_object_or_404(Proveedor, pk=proveedor_id) if proveedor_id else None

        Compra.objects.create(
            producto=prod,
            cantidad=cantidad,
            precio_total=precio_compra * cantidad,
            proveedor=proveedor,
        )

        messages.success(request, "Compra registrada.")
        return redirect("bodega:compras")

    ultimas = Compra.objects.select_related("producto", "proveedor").order_by("-fecha")[:25]

    return render(request, "compras.html", {
        "productos": productos,
        "proveedores": proveedores,
        "ultimas": ultimas,
    })

@login_required(login_url="/usuarios/login/")
def compras_editar(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method != "POST":
        return redirect("bodega:compras")

    cantidad_str = request.POST.get("cantidad", "").strip()
    precio_total_str = request.POST.get("precio_total", "").strip()

    if not cantidad_str.isdigit() or not precio_total_str.isdigit():
        messages.error(request, "Cantidad y precio total deben ser enteros.")
        return redirect("bodega:compras")

    nueva_cantidad = int(cantidad_str)
    nuevo_precio_total = int(precio_total_str)
    if nueva_cantidad <= 0 or nuevo_precio_total < 0:
        messages.error(request, "Valores inválidos.")
        return redirect("bodega:compras")

    delta = nueva_cantidad - compra.cantidad
    producto = compra.producto
    producto.stock = F("stock") + delta
    producto.save(update_fields=["stock"])

    compra.cantidad = nueva_cantidad
    compra.precio_total = nuevo_precio_total
    compra.save(update_fields=["cantidad", "precio_total"])

    messages.success(request, "Compra actualizada.")
    return redirect("bodega:compras")

@login_required(login_url="/usuarios/login/")
def compras_eliminar(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    producto = compra.producto
    producto.stock = F("stock") - compra.cantidad
    producto.save(update_fields=["stock"])
    compra.delete()
    messages.info(request, "Compra eliminada.")
    return redirect("bodega:compras")

# -------------------------
# Ventas
# -------------------------
@login_required(login_url="/usuarios/login/")
def ventas(request):
    productos = Producto.objects.order_by("nombre")
    carrito = _get_carrito(request)

    if request.method == "POST" and request.POST.get("accion") == "agregar":
        producto_id = request.POST.get("producto_id")
        cantidad = request.POST.get("cantidad", "1")
        tipo = request.POST.get("tipo", "minorista")

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError
        except Exception:
            messages.error(request, "Cantidad inválida.")
            return redirect("bodega:ventas")

        prod = get_object_or_404(Producto, pk=producto_id)

        if cantidad > prod.stock:
            messages.error(request, f"Stock insuficiente para {prod.nombre}. Stock: {prod.stock}")
            return redirect("bodega:ventas")

        for item in carrito:
            if item["producto_id"] == prod.id:
                item["cantidad"] += cantidad
                item["total"] = int(item["precio"]) * item["cantidad"]
                break
        else:
            precio = int(prod.precio_venta)
            carrito.append({
                "producto_id": prod.id,
                "producto": prod.nombre,
                "precio": precio,
                "cantidad": cantidad,
                "total": precio * cantidad,
                "tipo": tipo,
            })

        _guardar_carrito(request, carrito)
        messages.success(request, "Producto agregado al carrito.")
        return redirect("bodega:ventas")

    total_carrito = sum(int(i["total"]) for i in carrito) if carrito else 0

    return render(request, "ventas.html", {
        "productos": productos, "carrito": carrito, "total_carrito": total_carrito
    })

@login_required(login_url="/usuarios/login/")
def ventas_modificar_item(request, index):
    carrito = _get_carrito(request)
    if request.method == "POST" and 0 <= index < len(carrito):
        cantidad = request.POST.get("cantidad", "1")
        if cantidad.isdigit() and int(cantidad) > 0:
            carrito[index]["cantidad"] = int(cantidad)
            carrito[index]["total"] = int(carrito[index]["precio"]) * int(cantidad)
            _guardar_carrito(request, carrito)
            messages.info(request, "Ítem actualizado.")
        else:
            messages.error(request, "Cantidad inválida.")
    return redirect("bodega:ventas")

@login_required(login_url="/usuarios/login/")
def ventas_eliminar_item(request, index):
    carrito = _get_carrito(request)
    if 0 <= index < len(carrito):
        carrito.pop(index)
        _guardar_carrito(request, carrito)
        messages.info(request, "Ítem eliminado.")
    return redirect("bodega:ventas")

@login_required(login_url="/usuarios/login/")
def ventas_vaciar(request):
    request.session["carrito"] = []
    request.session.modified = True
    messages.info(request, "Carrito vaciado.")
    return redirect("bodega:ventas")

@login_required(login_url="/usuarios/login/")
@transaction.atomic
def confirmar_venta(request):
    carrito = _get_carrito(request)
    if not carrito:
        messages.error(request, "Carrito vacío.")
        return redirect("bodega:ventas")

    total = Decimal("0")
    ids = [i["producto_id"] for i in carrito]
    productos_cache = {p.id: p for p in Producto.objects.select_for_update().filter(id__in=ids)}

    for item in carrito:
        p = productos_cache[item["producto_id"]]
        if item["cantidad"] > p.stock:
            messages.error(request, f"Stock insuficiente para {p.nombre}.")
            return redirect("bodega:ventas")
        total += Decimal(item["precio"]) * item["cantidad"]

    venta = Venta.objects.create(total=total, tipo="minorista")

    for item in carrito:
        p = productos_cache[item["producto_id"]]
        DetalleVenta.objects.create(venta=venta, producto=p, cantidad=item["cantidad"])
        p.stock = F("stock") - item["cantidad"]
        p.save(update_fields=["stock"])

    request.session["carrito"] = []
    request.session.modified = True

    messages.success(request, f"Venta #{venta.id} confirmada.")
    return redirect("bodega:ventas")

# -------------------------
# Reportes
# -------------------------
@login_required(login_url="/usuarios/login/")
def reportes(request):
    hoy = timezone.localdate()

    detalles_con_subtotal = (
        DetalleVenta.objects
        .filter(venta__fecha__date=hoy)
        .annotate(
            subtotal=ExpressionWrapper(
                F("cantidad") * F("producto__precio_venta"),
                output_field=DecimalField(max_digits=18, decimal_places=0),
            )
        )
    )

    ventas_detalle_hoy = (
        detalles_con_subtotal
        .values("producto__id", "producto__nombre")
        .annotate(
            cantidad=Sum("cantidad"),
            total=Sum("subtotal"),
        )
        .order_by("-total")
    )

    total_ventas = ventas_detalle_hoy.aggregate(s=Sum("total"))["s"] or Decimal("0")

    compras_detalle_hoy = (
        Compra.objects.filter(fecha__date=hoy)
        .values("producto__id", "producto__nombre")
        .annotate(
            cantidad=Sum("cantidad"),
            total=Sum("precio_total"),
        )
        .order_by("-total")
    )
    total_compras = compras_detalle_hoy.aggregate(s=Sum("total"))["s"] or Decimal("0")

    return render(request, "reportes.html", {
        "total_ventas": total_ventas,
        "total_compras": total_compras,
        "ventas_detalle_hoy": ventas_detalle_hoy,
        "compras_detalle_hoy": compras_detalle_hoy,
    })
