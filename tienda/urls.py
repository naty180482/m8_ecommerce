from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("producto/<int:producto_id>/", views.detalle_producto, name="detalle_producto"),

    path("carrito/", views.carrito, name="carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_carrito, name="agregar_carrito"),
    path("carrito/actualizar/<int:producto_id>/", views.actualizar_carrito, name="actualizar_carrito"),
    path("carrito/eliminar/<int:producto_id>/", views.eliminar_carrito, name="eliminar_carrito"),

    path("checkout/confirmar/", views.confirmar_compra, name="confirmar_compra"),
    path("checkout/exito/<int:orden_id>/", views.compra_exitosa, name="compra_exitosa"),
    path("mis-pedidos/", views.mis_pedidos, name="mis_pedidos"),

    path("panel/productos/", views.admin_productos, name="admin_productos"),
    path("panel/productos/crear/", views.crear_producto, name="crear_producto"),
    path("panel/productos/editar/<int:producto_id>/", views.editar_producto, name="editar_producto"),
    path("panel/productos/eliminar/<int:producto_id>/", views.eliminar_producto, name="eliminar_producto"),

    path("logout/", views.logout_view, name="logout"),

]