from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Producto, PuebloMagico, MensajeContacto, Categoria, Favorito
from .forms import RegistroForm, ProductoForm

# --- Vistas Públicas ---

# Vista de la página de inicio
def inicio(request):
    pueblos = PuebloMagico.objects.all()[:3] # Recupera sólo los primeros 3 pueblos de la base de datos
    # Indicamos el lugar donde se renderiza el resultado de esta vista
    return render(request, 'catalogo/inicio.html', {'pueblos': pueblos})

# Vista de la página Acerca de
def acerca_de(request):
    return render(request, 'catalogo/acerca_de.html')

# Vista principal del catálogo de artesanías
def catalogo(request):
    productos = Producto.objects.all() # all recupera todos los registros de la tabla Producto
    pueblos = PuebloMagico.objects.all()
    categorias = Categoria.objects.all()
    
    # Obtenemos los valores de búsqueda desde la URL (lo que el usuario escribe o selecciona)
    pueblo_id = request.GET.get('pueblo')
    categoria_id = request.GET.get('categoria')
    q = request.GET.get('q')
    
    # Si hay filtros, aplicamos el filter correspondiente a los productos
    if pueblo_id:
        productos = productos.filter(municipio_origen_id=pueblo_id)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if q:
        productos = productos.filter(nombre__icontains=q) # __icontains busca coincidencias parciales de texto

    # Identificar favoritos si el usuario está logueado para mostrar el corazón pintado
    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_lista_obj = Favorito.objects.filter(usuario=request.user)
        # Llenamos la lista con los IDs usando un ciclo for clásico
        for fav in favoritos_lista_obj:
            favoritos_ids.append(fav.producto.id)

    # Diccionario con todos los datos que mandaremos al HTML
    context = {
        'productos': productos,
        'pueblos': pueblos,
        'categorias': categorias,
        'favoritos_ids': favoritos_ids,
        'pueblo_sel': int(pueblo_id) if pueblo_id else None,
        'cat_sel': int(categoria_id) if categoria_id else None,
        'q': q,
    }
    return render(request, 'catalogo/catalogo.html', context)

# Vista para ver los detalles de un producto específico
def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk) # Busca el producto por ID, si no existe marca error 404
    es_favorito = False
    if request.user.is_authenticated:
        # Verifica si existe un registro en favoritos para este usuario y producto
        es_favorito = Favorito.objects.filter(usuario=request.user, producto=producto).exists()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')
        
        if nombre and correo and mensaje:
            MensajeContacto.objects.create(
                nombre=nombre,
                correo=correo,
                tipo='comentario',
                mensaje=mensaje,
                producto=producto
            )
            messages.success(request, 'Comentario enviado exitosamente.')
            return redirect('producto_detalle', pk=pk)

    comentarios = MensajeContacto.objects.filter(producto=producto).order_by('-fecha_envio')
    
    return render(request, 'catalogo/producto_detalle.html', {
        'producto': producto,
        'es_favorito': es_favorito,
        'comentarios': comentarios
    })

# Vista para ver detalles de un pueblo y listar sus artesanías
def pueblo_detalle(request, pk):
    pueblo = get_object_or_404(PuebloMagico, pk=pk)
    # Filtra los productos que pertenecen al pueblo seleccionado
    productos = Producto.objects.filter(municipio_origen=pueblo)
    return render(request, 'catalogo/pueblo_detalle.html', {
        'pueblo': pueblo,
        'productos': productos
    })

# Vista para procesar el formulario de contacto
def contacto(request):
    if request.method == 'POST':
        # Captura los datos enviados en el formulario por método POST
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')
        tipo = 'duda'
        
        if nombre and correo and mensaje:
            # Crea e inserta directamente un nuevo registro en la base de datos
            MensajeContacto.objects.create(nombre=nombre, correo=correo, tipo=tipo, mensaje=mensaje, producto=None)
            messages.success(request, 'Mensaje enviado.')
            return redirect('contacto') # Redirecciona para evitar reenvío de formulario
    
    return render(request, 'catalogo/contacto.html')

# --- Favoritos ---

# Vista que lista solo los productos favoritos del usuario
def favoritos_lista(request):
    # Si no ha iniciado sesión, lo mandamos al login
    if not request.user.is_authenticated:
        return redirect('login')
    # Recupera todos sus favoritos de la tabla
    favoritos = Favorito.objects.filter(usuario=request.user)
    return render(request, 'catalogo/favoritos.html', {'favoritos': favoritos})

# Vista que procesa el click al ícono de corazón (agrega o quita favorito)
def toggle_favorito(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    producto = get_object_or_404(Producto, pk=pk)
    
    # Busca si el producto ya está en favoritos
    favoritos_guardados = Favorito.objects.filter(usuario=request.user, producto=producto)
    
    if favoritos_guardados:
        # Si ya existe, lo eliminamos
        favorito = favoritos_guardados[0]
        favorito.delete()
        messages.info(request, "Eliminado de favoritos.")
    else:
        # Si no existe, creamos e insertamos un nuevo registro
        favorito_nuevo = Favorito(usuario=request.user, producto=producto)
        favorito_nuevo.save()
        messages.success(request, "Añadido a favoritos.")
        
    # Funcionalidad para volver a la página donde estaba el usuario
    referer = request.META.get('HTTP_REFERER', 'catalogo')
    if referer and ('login' in referer or 'registro' in referer):
        return redirect('catalogo')
    return redirect(referer)

# --- Autenticación (Auth) ---

# Vista para crear una cuenta nueva
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid(): # Si los datos del formulario son correctos
            form.save() # Se inserta el nuevo usuario
            messages.success(request, 'Registro exitoso.')
            return redirect('login')
    else:
        # Si el método es GET, enviamos el formulario vacío
        form = RegistroForm()
    return render(request, 'catalogo/registro.html', {'form': form})

# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Realiza el inicio de sesión real en Django
            login(request, form.get_user())
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('catalogo')
    else:
        form = AuthenticationForm()
    return render(request, 'catalogo/login.html', {'form': form})

# Vista para cerrar la sesión
def logout_view(request):
    logout(request) # Destruye la sesión actual
    return redirect('inicio')

# --- Administración Simplificada ---

# Vista para listar los productos en formato tabla para administradores
def admin_lista(request):
    # Validación manual: si no es administrador (staff), mandarlo a inicio
    if not request.user.is_staff:
        return redirect('inicio')
    productos = Producto.objects.all()
    return render(request, 'catalogo/admin_lista.html', {'productos': productos})

# Vista para agregar una nueva artesanía
def admin_crear(request):
    if not request.user.is_staff:
        return redirect('inicio')
    if request.method == 'POST':
        # Procesamos el formulario incluyendo las imágenes (FILES)
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_lista')
    else:
        form = ProductoForm()
    return render(request, 'catalogo/admin_form.html', {'form': form, 'titulo': 'Agregar Producto'})

# Vista para modificar un registro existente
def admin_editar(request, pk):
    if not request.user.is_staff:
        return redirect('inicio')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        # Pasamos el parámetro "instance" para indicar que vamos a actualizar un objeto, no crear uno nuevo
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('admin_lista')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'catalogo/admin_form.html', {'form': form, 'titulo': 'Editar Producto'})

# Vista para borrar físicamente un producto
def admin_eliminar(request, pk):
    if not request.user.is_staff:
        return redirect('inicio')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST': # Opcionalmente se podría usar POST para confirmar
        pass
    # Se elimina de la base de datos permanentemente
    producto.delete()
    return redirect('admin_lista')
