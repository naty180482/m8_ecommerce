from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, ProductoForm
from .models import Categoria, DetalleOrden, Orden, Producto


def es_admin(user):
    return user.is_authenticated and user.is_staff


class UsuarioLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm


def home(request):
    productos_destacados = Producto.objects.filter(activo=True, destacado=True)[:6]
    categorias = Categoria.objects.all()
    return render(request, "tienda/home.html", {
        "productos_destacados": productos_destacados,
        "categorias": categorias
    })


def catalogo(request):
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.all()

    categoria_id = request.GET.get("categoria")
    buscar = request.GET.get("buscar")

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    return render(request, "tienda/catalogo.html", {
        "productos": productos,
        "categorias": categorias,
        "categoria_id": categoria_id,
        "buscar": buscar or ""
    })


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    return render(request, "tienda/detalle_producto.html", {
        "producto": producto
    })


@login_required
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)

    if producto.stock <= 0:
        messages.error(request, "El producto no tiene stock disponible.")
        return redirect("detalle_producto", producto_id=producto.id)

    cantidad = int(request.POST.get("cantidad", 1))

    if cantidad <= 0:
        messages.error(request, "La cantidad debe ser mayor a 0.")
        return redirect("detalle_producto", producto_id=producto.id)

    if cantidad > producto.stock:
        messages.error(request, "La cantidad solicitada supera el stock disponible.")
        return redirect("detalle_producto", producto_id=producto.id)

    carrito = request.session.get("carrito", {})
    producto_key = str(producto.id)

    if producto_key in carrito:
        nueva_cantidad = carrito[producto_key]["cantidad"] + cantidad
        if nueva_cantidad > producto.stock:
            messages.error(request, "No puedes agregar más unidades que el stock disponible.")
            return redirect("carrito")
        carrito[producto_key]["cantidad"] = nueva_cantidad
    else:
        carrito[producto_key] = {
            "nombre": producto.nombre,
            "precio": str(producto.precio),
            "cantidad": cantidad,
        }

    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(request, "Producto agregado al carrito.")
    return redirect("carrito")


@login_required
def carrito(request):
    carrito = request.session.get("carrito", {})
    items = []
    total = Decimal("0")

    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        precio = Decimal(item["precio"])
        cantidad = item["cantidad"]
        subtotal = precio * cantidad
        total += subtotal

        items.append({
            "producto": producto,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal,
        })

    return render(request, "tienda/carrito.html", {
        "items": items,
        "total": total
    })


@login_required
def actualizar_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})
    producto = get_object_or_404(Producto, id=producto_id)
    producto_key = str(producto_id)

    if producto_key not in carrito:
        messages.error(request, "El producto no existe en el carrito.")
        return redirect("carrito")

    cantidad = int(request.POST.get("cantidad", 1))

    if cantidad <= 0:
        messages.error(request, "La cantidad debe ser mayor a 0.")
        return redirect("carrito")

    if cantidad > producto.stock:
        messages.error(request, "La cantidad supera el stock disponible.")
        return redirect("carrito")

    carrito[producto_key]["cantidad"] = cantidad
    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(request, "Carrito actualizado.")
    return redirect("carrito")


@login_required
def eliminar_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})
    producto_key = str(producto_id)

    if producto_key in carrito:
        del carrito[producto_key]
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, "Producto eliminado del carrito.")

    return redirect("carrito")


@login_required
@transaction.atomic
def confirmar_compra(request):
    carrito = request.session.get("carrito", {})

    if not carrito:
        messages.error(request, "El carrito está vacío.")
        return redirect("catalogo")

    total = Decimal("0")
    productos_compra = []

    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id, activo=True)
        cantidad = item["cantidad"]

        if cantidad > producto.stock:
            messages.error(request, f"No hay stock suficiente para {producto.nombre}.")
            return redirect("carrito")

        precio = Decimal(item["precio"])
        subtotal = precio * cantidad
        total += subtotal

        productos_compra.append((producto, cantidad, precio))

    orden = Orden.objects.create(
        usuario=request.user,
        total=total,
        estado="confirmada"
    )

    for producto, cantidad, precio in productos_compra:
        DetalleOrden.objects.create(
            orden=orden,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio
        )
        producto.stock -= cantidad
        producto.save()

    request.session["carrito"] = {}
    request.session.modified = True

    messages.success(request, "Compra confirmada correctamente.")
    return redirect("compra_exitosa", orden_id=orden.id)


@login_required
def compra_exitosa(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id, usuario=request.user)
    return render(request, "tienda/compra_exitosa.html", {
        "orden": orden
    })


@login_required
def mis_pedidos(request):
    ordenes = Orden.objects.filter(usuario=request.user)
    return render(request, "tienda/mis_pedidos.html", {
        "ordenes": ordenes
    })


@user_passes_test(es_admin)
def admin_productos(request):
    productos = Producto.objects.all()
    return render(request, "tienda/admin_productos.html", {
        "productos": productos
    })


@user_passes_test(es_admin)
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("admin_productos")
    else:
        form = ProductoForm()

    return render(request, "tienda/producto_form.html", {
        "form": form,
        "titulo": "Crear producto"
    })


@user_passes_test(es_admin)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("admin_productos")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "tienda/producto_form.html", {
        "form": form,
        "titulo": "Editar producto"
    })


@user_passes_test(es_admin)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("admin_productos")

    return render(request, "tienda/producto_confirm_delete.html", {
        "producto": producto
    })


def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("home")