from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import io
import os
from django.core.files.base import ContentFile


def _convertir_webp(image_field, max_ancho=1200, max_alto=1200, calidad=82):
    """Convierte un ImageField a WebP comprimido y redimensionado."""
    if not image_field:
        return
    try:
        img = Image.open(image_field)
        # Convertir a RGB (necesario para WebP, elimina canal alpha si existe)
        img = img.convert('RGB')
        # Redimensionar manteniendo proporción si es demasiado grande
        img.thumbnail((max_ancho, max_alto), Image.LANCZOS)
        # Guardar como WebP en memoria
        output = io.BytesIO()
        img.save(output, format='WEBP', quality=calidad, method=6)
        output.seek(0)
        # Construir el nuevo nombre con extensión .webp
        base_name = os.path.splitext(os.path.basename(image_field.name))[0]
        nuevo_nombre = f"{base_name}.webp"
        image_field.save(nuevo_nombre, ContentFile(output.read()), save=False)
    except Exception:
        pass  # Si falla la conversión, dejamos la imagen original


# Modelo para registrar la información de los Pueblos Mágicos
class PuebloMagico(models.Model): # Define la estructura de nuestra tabla PuebloMagico
    nombre = models.CharField(max_length=100) # Texto corto
    estado = models.CharField(max_length=100) # Texto corto
    imagen = models.ImageField(upload_to='pueblos/', null=True, blank=True) # Campo para subir fotografías
    historia = models.TextField(null=True, blank=True) # Texto largo
    ubicacion = models.CharField(max_length=255, null=True, blank=True)
    descripcion_cultural = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Si se subió una imagen nueva que no es WebP, convertirla
        if self.imagen and not self.imagen.name.endswith('.webp'):
            _convertir_webp(self.imagen, max_ancho=900, max_alto=600)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre # Indica que se mostrará el nombre como valor al imprimir este objeto

# Modelo para guardar las categorías de los productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo principal para registrar las Artesanías
class Producto(models.Model):
    nombre = models.CharField(max_length=200) # Nombre de la artesanía
    descripcion = models.TextField() # Texto largo para la descripción
    fotografia = models.ImageField(upload_to='productos/') # Fotografía del producto
    municipio_origen = models.ForeignKey(PuebloMagico, on_delete=models.CASCADE) # Llave foránea (relación con PuebloMagico)
    estado = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2) # Campo numérico con decimales
    material = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) # Llave foránea (relación con Categoria)

    def save(self, *args, **kwargs):
        # Si se subió una imagen nueva que no es WebP, convertirla
        if self.fotografia and not self.fotografia.name.endswith('.webp'):
            _convertir_webp(self.fotografia, max_ancho=800, max_alto=800)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Modelo para guardar la información del formulario de contacto
class MensajeContacto(models.Model):
    # Opciones de selección para el tipo de mensaje
    TIPO_MENSAJE_CHOICES = [
        ('duda', 'Duda General'),
        ('comentario', 'Comentario de Producto'),
    ]
    nombre = models.CharField(max_length=150)
    correo = models.EmailField() # Campo especial para validar correos
    tipo = models.CharField(max_length=20, choices=TIPO_MENSAJE_CHOICES)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True) # Fecha y tiempo exacto, se llena automático

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"

# Modelo para guardar las artesanías favoritas de cada usuario
class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Relación con el usuario registrado
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) # Relación con el producto favorito
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Evita que un mismo usuario guarde el mismo producto dos veces
        unique_together = ('usuario', 'producto')

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"
