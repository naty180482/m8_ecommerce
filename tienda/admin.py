from django.contrib import admin
from .models import Categoria, Producto, Orden, DetalleOrden


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria", "precio", "stock", "activo", "destacado")
    list_filter = ("categoria", "activo", "destacado")
    search_fields = ("nombre", "descripcion")
    list_editable = ("precio", "stock", "activo", "destacado")


class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 0
    readonly_fields = ("producto", "cantidad", "precio_unitario")


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "fecha", "total", "estado")
    list_filter = ("estado", "fecha")
    search_fields = ("usuario__username",)
    inlines = [DetalleOrdenInline]