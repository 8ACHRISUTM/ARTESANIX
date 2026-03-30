from django.contrib import admin
from .models import PuebloMagico, Categoria, Producto, MensajeContacto

@admin.register(PuebloMagico)
class PuebloMagicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    search_fields = ('nombre', 'estado')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo', 'municipio_origen', 'categoria', 'estado')
    list_filter = ('municipio_origen', 'categoria', 'estado', 'material')
    search_fields = ('nombre', 'descripcion')

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'tipo', 'fecha_envio')
    list_filter = ('tipo', 'fecha_envio')
    search_fields = ('nombre', 'correo', 'mensaje')
