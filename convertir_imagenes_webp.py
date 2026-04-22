"""
Script para convertir imágenes existentes de productos y pueblos a WebP.
Ejecutar UNA VEZ en PythonAnywhere con:
    cd ~/ARTESANIX
    python convertir_imagenes_webp.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artesanix_project.settings')
django.setup()

from PIL import Image
import io
from django.core.files.base import ContentFile
from catalogo.models import Producto, PuebloMagico


def convertir_a_webp(image_field, max_ancho, max_alto, calidad=82):
    if not image_field or image_field.name.endswith('.webp'):
        return False
    try:
        img = Image.open(image_field.path)
        img = img.convert('RGB')
        img.thumbnail((max_ancho, max_alto), Image.LANCZOS)
        output = io.BytesIO()
        img.save(output, format='WEBP', quality=calidad, method=6)
        output.seek(0)
        base_name = os.path.splitext(os.path.basename(image_field.name))[0]
        nuevo_nombre = f"{base_name}.webp"
        image_field.save(nuevo_nombre, ContentFile(output.read()), save=False)
        return True
    except Exception as e:
        print(f"  ⚠ Error: {e}")
        return False


print("=" * 50)
print("Convirtiendo imágenes de Productos a WebP...")
print("=" * 50)
productos = Producto.objects.exclude(fotografia='')
for p in productos:
    print(f"  → {p.nombre}: {p.fotografia.name}")
    if convertir_a_webp(p.fotografia, 800, 800):
        p.save(update_fields=['fotografia'])
        print(f"    ✓ Convertido → {p.fotografia.name}")
    else:
        print(f"    - Ya es WebP o sin imagen")

print()
print("=" * 50)
print("Convirtiendo imágenes de Pueblos Mágicos a WebP...")
print("=" * 50)
pueblos = PuebloMagico.objects.exclude(imagen='').exclude(imagen=None)
for p in pueblos:
    print(f"  → {p.nombre}: {p.imagen.name}")
    if convertir_a_webp(p.imagen, 900, 600):
        p.save(update_fields=['imagen'])
        print(f"    ✓ Convertido → {p.imagen.name}")
    else:
        print(f"    - Ya es WebP o sin imagen")

print()
print("✅ ¡Conversión completa!")
