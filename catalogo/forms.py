from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from .models import Producto

# Formulario para registrar usuarios nuevos, hereda las funciones básicas de Django
class RegistroForm(UserCreationForm):
    # Clase Meta especifica el modelo base para el formulario
    class Meta:
        model = User
        fields = ("username", "email") # Campos que le vamos a pedir al usuario

    # Método para inicializar el formulario con nuestros atributos CSS personalizados
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Ejecuta el inicializador original
        
        # Recorre todos los campos para quitar textos largos de ayuda y asignar clases CSS
        for field_name, field in self.fields.items():
            field.help_text = ''
            field.widget.attrs.update({'class': 'form-control'})
        
        # Validamos que el correo sea un dato obligatorio antes de guardar
        if 'email' in self.fields:
            self.fields['email'].required = True

# Formulario para agregar y editar registros de Productos desde el panel admin
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__' # Indicamos que tomará absolutamente todos los datos de la base
        
        # Diccionario widgets: Personaliza qué se dibuja en el HTML y le añade estilos de Bootstrap
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), # Area de texto de 4 filas
            'fotografia': forms.ClearableFileInput(attrs={'class': 'form-control'}), # Campo para archivo multimedia
            'municipio_origen': forms.Select(attrs={'class': 'form-control'}), # Lista select
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }
