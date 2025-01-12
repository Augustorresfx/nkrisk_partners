from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator

# Importe Modelos
from .models import Matriz, Broker, Aseguradora

# 404 page
def pagina_no_encontrada(request, exception):
    
    return HttpResponseNotFound(render(request, '404.html'))

# Home solo redirecciona al login
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, 'index.html', context)
    
# Inicio
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.groups.filter(name='PermisoBasico').exists() or user.is_staff), name='dispatch')
class InicioView(View):
    def get(self, request, *args, **kwargs):
        
        context = {
            
        }
        return render(request, 'dashboard.html', context)
    
# Matríz
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.groups.filter(name='PermisoBasico').exists() or user.is_staff), name='dispatch')
class MatrizView(View):
    def get(self, request, *args, **kwargs):
        matrices = Matriz.objects.all()
        
        matrices_paginados = Paginator(matrices, 30)
        page_number = request.GET.get("page")
        filter_pages = matrices_paginados.get_page(page_number)

        context = {
            'matrices': matrices, 
            'pages': filter_pages,

        }
        return render(request, 'matrices.html', context)
    def post(self, request, *args, **kwargs):
        # Obtener los datos del formulario directamente desde request.POST
        
        nombre = request.POST.get('nombre')
        pais = request.POST.get('pais')
        activo = request.POST.get('activo')
        

        # Crea una nueva instancia de Matriz
        nueva_matriz = Matriz(
            
            nombre=nombre,
            pais=pais,
            activo=activo,
            
        )
        try:
            # Intenta crear el nuevo elemento
            nueva_matriz.save()
            messages.success(request, 'El elemento se creó exitosamente.')
        except Exception as e:
            # Si hay un error al crear el elemento, captura la excepción
            messages.error(request, f'Error: No se pudo crear el elemento. Detalles: {str(e)}')

        # Redirige, incluyendo los mensajes en el contexto
        return HttpResponseRedirect(request.path_info)
        
    
    
    
# Autenticación
class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class SignInView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('inicio')
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
        
        return render(request, 'login.html', {
            'form': form,
            'error': 'El nombre de usuario o la contraseña no existen',
        })
        