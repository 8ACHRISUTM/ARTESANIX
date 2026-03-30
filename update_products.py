import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artesanix_project.settings')
django.setup()

from catalogo.models import PuebloMagico, Categoria, Producto

# 1. Delete previous generic products created
nombres_viejos = [
    'Jarra de Barro Rojo',
    'Vasos de Vidrio Soplado',
    'Plato Decorativo de Talavera',
    'Catrina de Cartonería',
    'Bolso Bordado a Mano',
    'Suéter de Lana Tradicional',
    'Canasta de Carrizo',
    'Alebrije de Madera',
    'Rebozo Fino de Algodón',
    'Juego de Tazas de Barro'
]

Producto.objects.filter(nombre__in=nombres_viejos).delete()

# 2. Add or Get Pueblos Magicos Authenticos
pueblos_data = [
    {"nombre": "Metepec", "estado": "Estado de México"},
    {"nombre": "Chignahuapan", "estado": "Puebla"},
    {"nombre": "Taxco de Alarcón", "estado": "Guerrero"},
    {"nombre": "Santa María del Río", "estado": "San Luis Potosí"},
    {"nombre": "San Miguel de Allende", "estado": "Guanajuato"},
    {"nombre": "Paracho de Buenavista", "estado": "Michoacán"},
    {"nombre": "Tequisquiapan", "estado": "Querétaro"},
    {"nombre": "Cholula", "estado": "Puebla"},
    {"nombre": "Tzintzuntzan", "estado": "Michoacán"},
    {"nombre": "Tlalpujahua de Rayón", "estado": "Michoacán"},
]

pueblos = {}
for p in pueblos_data:
    obj, created = PuebloMagico.objects.get_or_create(nombre=p['nombre'], defaults={'estado': p['estado']})
    pueblos[p['nombre']] = obj

# 3. Add Categories
cat_ceramica, _ = Categoria.objects.get_or_create(nombre="Cerámica")
cat_vidrio, _ = Categoria.objects.get_or_create(nombre="Vidrio")
cat_metal, _ = Categoria.objects.get_or_create(nombre="Metalistería")
cat_textiles, _ = Categoria.objects.get_or_create(nombre="Textiles")
cat_madera, _ = Categoria.objects.get_or_create(nombre="Laudería")
cat_fibras, _ = Categoria.objects.get_or_create(nombre="Fibras Vegetales")

# 4. Insert 10 Authentic Products
productos = [
    {
        'nombre': 'Árbol de la Vida',
        'descripcion': 'Colorida escultura de barro policromado, representativa de las tradiciones y el imaginario mexicano.',
        'municipio_origen': pueblos['Metepec'],
        'estado': pueblos['Metepec'].estado,
        'costo': 2500.00,
        'material': 'Barro policromado',
        'categoria': cat_ceramica,
        'fotografia': 'productos/basija.jpeg'
    },
    {
        'nombre': 'Esferas Navideñas Sopladas',
        'descripcion': 'Set de esferas de vidrio soplado, decoradas a mano con gran detalle.',
        'municipio_origen': pueblos['Chignahuapan'],
        'estado': pueblos['Chignahuapan'].estado,
        'costo': 350.00,
        'material': 'Vidrio soplado',
        'categoria': cat_vidrio,
        'fotografia': 'productos/vasija1.jpeg'
    },
    {
        'nombre': 'Joyería Fina de Plata',
        'descripcion': 'Elegante collar y aretes de plata ley .925 con diseño artesanal.',
        'municipio_origen': pueblos['Taxco de Alarcón'],
        'estado': pueblos['Taxco de Alarcón'].estado,
        'costo': 1800.00,
        'material': 'Plata .925',
        'categoria': cat_metal,
        'fotografia': 'productos/basija.jpeg'
    },
    {
        'nombre': 'Rebozo de Seda de Bolita',
        'descripcion': 'Hermoso rebozo tejido a mano en telar de cintura, famoso por pasar por el ojal de un anillo.',
        'municipio_origen': pueblos['Santa María del Río'],
        'estado': pueblos['Santa María del Río'].estado,
        'costo': 4500.00,
        'material': 'Seda',
        'categoria': cat_textiles,
        'fotografia': 'productos/playera.jpeg'
    },
    {
        'nombre': 'Corazón de Latón Repujado',
        'descripcion': 'Corazón tradicional de latón trabajado a mano, ideal para decoración de interiores.',
        'municipio_origen': pueblos['San Miguel de Allende'],
        'estado': pueblos['San Miguel de Allende'].estado,
        'costo': 450.00,
        'material': 'Latón',
        'categoria': cat_metal,
        'fotografia': 'productos/vasija1.jpeg'
    },
    {
        'nombre': 'Guitarra de Concierto',
        'descripcion': 'Guitarra fina elaborada por lauderos expertos con maderas preciosas e incrustaciones.',
        'municipio_origen': pueblos['Paracho de Buenavista'],
        'estado': pueblos['Paracho de Buenavista'].estado,
        'costo': 8500.00,
        'material': 'Palo escrito y pino',
        'categoria': cat_madera,
        'fotografia': 'productos/basija.jpeg'
    },
    {
        'nombre': 'Cesta de Mimbre y Vara',
        'descripcion': 'Cesta utilitaria y resistente tejida a mano con técnicas tradicionales.',
        'municipio_origen': pueblos['Tequisquiapan'],
        'estado': pueblos['Tequisquiapan'].estado,
        'costo': 280.00,
        'material': 'Mimbre y vara',
        'categoria': cat_fibras,
        'fotografia': 'productos/vasija1.jpeg'
    },
    {
        'nombre': 'Tiborcito de Talavera',
        'descripcion': 'Jarrón de auténtica Talavera con denominación de origen, pintado con motivos tradicionales.',
        'municipio_origen': pueblos['Cholula'],
        'estado': pueblos['Cholula'].estado,
        'costo': 1200.00,
        'material': 'Cerámica Mayólica (Talavera)',
        'categoria': cat_ceramica,
        'fotografia': 'productos/basija.jpeg'
    },
    {
        'nombre': 'Centro de Mesa de Chuspata',
        'descripcion': 'Artesanía tejida con fibras de lago (chuspata), ideal para decoración rústica.',
        'municipio_origen': pueblos['Tzintzuntzan'],
        'estado': pueblos['Tzintzuntzan'].estado,
        'costo': 400.00,
        'material': 'Chuspata',
        'categoria': cat_fibras,
        'fotografia': 'productos/vasija1.jpeg'
    },
    {
        'nombre': 'Esfera de Arte Plumario',
        'descripcion': 'Esfera decorativa detallada con el delicado e histórico arte plumario michoacano.',
        'municipio_origen': pueblos['Tlalpujahua de Rayón'],
        'estado': pueblos['Tlalpujahua de Rayón'].estado,
        'costo': 850.00,
        'material': 'Vidrio y plumas',
        'categoria': cat_vidrio,
        'fotografia': 'productos/vasija1.jpeg'
    }
]

for p in productos:
    Producto.objects.create(**p)

print(f"Borrados productos antiguos. {len(productos)} productos reales creados exitosamente.")
