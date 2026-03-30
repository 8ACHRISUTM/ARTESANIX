import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artesanix_project.settings')
django.setup()

from catalogo.models import PuebloMagico, Categoria, Producto

# 1: Acambaro, 2: Pátzcuaro, 3: Yuriria, 4: Tacámbaro
pueblos = list(PuebloMagico.objects.all())

cat_textiles, _ = Categoria.objects.get_or_create(nombre='Textiles')
cat_ceramica, _ = Categoria.objects.get_or_create(nombre='Cerámica')
cat_vidrio, _ = Categoria.objects.get_or_create(nombre='Vidrio')
cat_madera, _ = Categoria.objects.get_or_create(nombre='Madera')
cat_fibras, _ = Categoria.objects.get_or_create(nombre='Fibras Vegetales')
cat_carton, _ = Categoria.objects.get_or_create(nombre='Papel y Cartón')

productos = [
    {
        'nombre': 'Jarra de Barro Rojo',
        'descripcion': 'Hermosa jarra artesanal perfecta para servir agua fresca.',
        'municipio_origen': pueblos[1] if len(pueblos)>1 else pueblos[0],
        'estado': pueblos[1].estado if len(pueblos)>1 else pueblos[0].estado,
        'costo': 250.00,
        'material': 'Barro rojo',
        'categoria': cat_ceramica,
        'fotografia': 'productos/vasija1.jpeg'
    },
    {
        'nombre': 'Vasos de Vidrio Soplado',
        'descripcion': 'Set de 4 vasos artesanales con borde azul.',
        'municipio_origen': pueblos[3] if len(pueblos)>3 else pueblos[0],
        'estado': pueblos[3].estado if len(pueblos)>3 else pueblos[0].estado,
        'costo': 320.00,
        'material': 'Vidrio',
        'categoria': cat_vidrio,
        'fotografia': 'productos/vasija1.jpeg'
    },
    {
        'nombre': 'Plato Decorativo de Talavera',
        'descripcion': 'Plato adornado con hermosos y coloridos motivos.',
        'municipio_origen': pueblos[2] if len(pueblos)>2 else pueblos[0],
        'estado': pueblos[2].estado if len(pueblos)>2 else pueblos[0].estado,
        'costo': 450.00,
        'material': 'Cerámica',
        'categoria': cat_ceramica,
        'fotografia': 'productos/basija.jpeg'
    },
    {
        'nombre': 'Catrina de Cartonería',
        'descripcion': 'Figura tradicional del día de muertos hecha en cartonería.',
        'municipio_origen': pueblos[0],
        'estado': pueblos[0].estado,
        'costo': 500.00,
        'material': 'Papel y cartón',
        'categoria': cat_carton,
        'fotografia': 'productos/basija.jpeg'
    },
    {
        'nombre': 'Bolso Bordado a Mano',
        'descripcion': 'Bolso de tela resistente con bordado tradicional en colores vibrantes.',
        'municipio_origen': pueblos[1] if len(pueblos)>1 else pueblos[0],
        'estado': pueblos[1].estado if len(pueblos)>1 else pueblos[0].estado,
        'costo': 600.00,
        'material': 'Textil',
        'categoria': cat_textiles,
        'fotografia': 'productos/playera.jpeg'
    },
    {
        'nombre': 'Suéter de Lana Tradicional',
        'descripcion': 'Suéter cálido tejido a mano para las épocas de frío.',
        'municipio_origen': pueblos[2] if len(pueblos)>2 else pueblos[0],
        'estado': pueblos[2].estado if len(pueblos)>2 else pueblos[0].estado,
        'costo': 850.00,
        'material': 'Lana',
        'categoria': cat_textiles,
        'fotografia': 'productos/playera.jpeg'
    },
    {
        'nombre': 'Canasta de Carrizo',
        'descripcion': 'Canasta multiusos de fibras naturales tejida elaboradamente.',
        'municipio_origen': pueblos[3] if len(pueblos)>3 else pueblos[0],
        'estado': pueblos[3].estado if len(pueblos)>3 else pueblos[0].estado,
        'costo': 180.00,
        'material': 'Carrizo',
        'categoria': cat_fibras,
        'fotografia': 'productos/basija.jpeg'
    },
    {
        'nombre': 'Alebrije de Madera',
        'descripcion': 'Figura de fantasia de madera tallada y pintada.',
        'municipio_origen': pueblos[0],
        'estado': pueblos[0].estado,
        'costo': 950.00,
        'material': 'Madera',
        'categoria': cat_madera,
        'fotografia': 'productos/basija.jpeg'
    },
    {
        'nombre': 'Rebozo Fino de Algodón',
        'descripcion': 'Prenda tradicional mexicana tejida en telar.',
        'municipio_origen': pueblos[1] if len(pueblos)>1 else pueblos[0],
        'estado': pueblos[1].estado if len(pueblos)>1 else pueblos[0].estado,
        'costo': 1200.00,
        'material': 'Algodón',
        'categoria': cat_textiles,
        'fotografia': 'productos/playera.jpeg'
    },
    {
        'nombre': 'Juego de Tazas de Barro',
        'descripcion': 'Perfectas para un café de olla caliente.',
        'municipio_origen': pueblos[2] if len(pueblos)>2 else pueblos[0],
        'estado': pueblos[2].estado if len(pueblos)>2 else pueblos[0].estado,
        'costo': 280.00,
        'material': 'Barro bruñido',
        'categoria': cat_ceramica,
        'fotografia': 'productos/vasija1.jpeg'
    }
]

for p in productos:
    Producto.objects.create(**p)

print(f"{len(productos)} productos creados exitosamente.")
