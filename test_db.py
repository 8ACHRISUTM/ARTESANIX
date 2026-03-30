import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artesanix_project.settings')
django.setup()

from catalogo.models import PuebloMagico, Categoria, Producto

print("Pueblos Mágicos:")
for p in PuebloMagico.objects.all():
    print(f"{p.id}: {p.nombre} - {p.estado}")

print("\nCategorías:")
for c in Categoria.objects.all():
    print(f"{c.id}: {c.nombre}")

print("\nProductos:")
for p in Producto.objects.all():
    print(f"{p.id}: {p.nombre}")
