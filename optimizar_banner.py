"""
Script para convertir el banner PNG de 8MB a WebP optimizado.
Copiar a static/img/ para ser servido con cache por Whitenoise.

Ejecutar en PythonAnywhere:
    cd ~/ARTESANIX
    python optimizar_banner.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artesanix_project.settings')
django.setup()

from PIL import Image
from django.conf import settings

# --- 1. Convertir el banner PNG gigante ---
banner_origen = os.path.join(settings.MEDIA_ROOT, 'productos', 'Gemini_Generated_Image_llcgv8llcgv8llcg.png')
banner_destino = os.path.join(settings.BASE_DIR, 'static', 'img', 'hero_bg.webp')

if os.path.exists(banner_origen):
    print(f"Convirtiendo banner ({os.path.getsize(banner_origen) // 1024} KB)...")
    img = Image.open(banner_origen).convert('RGB')
    # Redimensionar a max 1600px de ancho (más que suficiente para desktop)
    img.thumbnail((1600, 800), Image.LANCZOS)
    img.save(banner_destino, 'WEBP', quality=70, method=6)
    print(f"✓ Banner guardado en static/img/hero_bg.webp ({os.path.getsize(banner_destino) // 1024} KB)")
else:
    print(f"⚠ No se encontró el banner en: {banner_origen}")

# --- 2. Convertir logo.png a WebP ---
logo_origen = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png')
logo_destino = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.webp')

if os.path.exists(logo_origen):
    print(f"\nConvirtiendo logo ({os.path.getsize(logo_origen) // 1024} KB)...")
    img = Image.open(logo_origen).convert('RGBA')
    # Redimensionar a un máximo de 360x360 (se muestra a 65px de alto)
    img.thumbnail((360, 360), Image.LANCZOS)
    # WebP soporta transparencia (RGBA)
    img.save(logo_destino, 'WEBP', quality=80, method=6)
    print(f"✓ Logo guardado en static/img/logo.webp ({os.path.getsize(logo_destino) // 1024} KB)")
else:
    print(f"⚠ No se encontró el logo en: {logo_origen}")

print("\n✅ Listo. Ejecuta ahora:")
print("   python manage.py collectstatic --noinput")
