from django.urls import path
from . import views

# Lista de rutas y enlaces de nuestra aplicación
urlpatterns = [
    # Rutas Públicas accesibles por todos
    path('', views.catalogo, name='inicio'), # Ruta de la página de inicio original, redirige al catálogo
    path('catalogo/', views.catalogo, name='catalogo'), # Enlace principal de las artesanías
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'), # <int:pk> lee el ID dinámico de la base de datos
    path('pueblo/<int:pk>/', views.pueblo_detalle, name='pueblo_detalle'),
    
    # Rutas de Marcado de Favoritos
    path('favoritos/', views.favoritos_lista, name='favoritos_lista'),
    path('favoritos/toggle/<int:pk>/', views.toggle_favorito, name='toggle_favorito'), # Acción que guarda o borra el favorito
    
    # Rutas informativas
    path('contacto/', views.contacto, name='contacto'), # Enlace al formulario de dudas o comentarios
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    
    # Rutas de Cuentas de Usuarios
    path('registro/', views.registro, name='registro'), # Enlace de creación de cuenta
    path('login/', views.login_view, name='login'), # Enlace para entrar
    path('logout/', views.logout_view, name='logout'), # Enlace para salir 
    
    # Rutas de Administración (Solo personal)
    path('admin-artesanix/', views.admin_lista, name='admin_lista'),
    path('admin-artesanix/nuevo/', views.admin_crear, name='admin_crear'), # Ruta para agregar un registro
    path('admin-artesanix/editar/<int:pk>/', views.admin_editar, name='admin_editar'), # Ruta para editarlo
    path('admin-artesanix/eliminar/<int:pk>/', views.admin_eliminar, name='admin_eliminar'), # Acción de borrado
]