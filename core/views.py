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
from django.shortcuts import redirect
from django.apps import apps

# Importe Modelos
from .models import Pais, Matriz, Broker, Aseguradora, PendingChange

# Usuarios / roles
def is_admin(user):
    return user.is_superuser

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
class InicioView(View):
    def get(self, request, *args, **kwargs):
        
        context = {
            
        }
        return render(request, 'dashboard.html', context)
    
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin, login_url='/login '), name='dispatch')
class CambiosPendientesView(View):
    def get(self, request, *args, **kwargs):
        changes = PendingChange.objects.filter(approved__isnull=True)

        for change in changes:
            change.is_deletion = change.action_type == 'delete'  # Agrega un atributo al objeto

        context = {
            'changes': changes
        }

        return render(request, 'cambios.html', context=context)

    
# Matríz
@method_decorator(login_required, name='dispatch')
class MatrizView(View):
    def get(self, request, *args, **kwargs):
        matrices = Matriz.objects.all()
        print(matrices)
        matrices_paginados = Paginator(matrices, 30)
        page_number = request.GET.get("page")
        filter_pages = matrices_paginados.get_page(page_number)
        paises = Pais.objects.all()
        context = {
            'matrices': matrices, 
            'pages': filter_pages,
            'paises': paises,

        }
        return render(request, 'matrices.html', context)
    def post(self, request, *args, **kwargs):
        # Obtener los datos del formulario directamente desde request.POST
        
        nombre = request.POST.get('nuevo_nombre')
        pais_id = request.POST.get('nuevo_pais')
        activo = request.POST.get('nuevo_activo')
        print(f"Activo recibido: {activo}")
        pais = get_object_or_404(Pais, id=pais_id)
        user = request.user
        # Crea una nueva instancia de Matriz
        nueva_matriz = Matriz(
            
            nombre=nombre,
            pais=pais,
            activo=activo,
            modified_by=user,
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
    
@method_decorator(login_required, name='dispatch')
class EditarMatrizView(View):
    def post(self, request, matriz_id):
        matriz = get_object_or_404(Matriz, id=matriz_id)
        nombre = request.POST.get('editar_nombre')
        pais_id = request.POST.get('editar_pais')
        activo = 'editar_activo' in request.POST
        user = request.user

        # Si el usuario es superuser, aplicar los cambios directamente
        if user.is_superuser:
            if matriz.nombre != nombre:
                matriz.nombre = nombre
            if matriz.pais_id != int(pais_id):
                matriz.pais_id = pais_id
            if matriz.activo != activo:
                matriz.activo = activo

            matriz.save()  # Guardar los cambios directamente
            messages.success(request, 'Los cambios se han aplicado directamente.')
            return redirect('matrices')

        # Para usuarios no superuser, registrar los cambios pendientes
        changes = {}
        if matriz.nombre != nombre:
            changes['nombre'] = {'old': matriz.nombre, 'new': nombre}
            matriz.nombre = nombre

        if matriz.pais_id != int(pais_id):
            changes['pais'] = {'old': matriz.pais_id, 'new': int(pais_id)}
            matriz.pais_id = pais_id

        if matriz.activo != activo:
            changes['activo'] = {'old': matriz.activo, 'new': activo}
            matriz.activo = activo

        if changes:
            try:
                PendingChange.objects.create(
                    model_name='matriz',
                    object_id=matriz.id,
                    changes=changes,
                    submitted_by=user,
                    action_type='edit'
                )
                messages.success(request, 'El cambio ha sido registrado para revisión.')
            except Exception as e:
                messages.error(request, f'Error al registrar el cambio: {str(e)}')
        else:
            messages.info(request, 'No se detectaron cambios.')

        return redirect('matrices')


@method_decorator(login_required, name='dispatch')
class EliminarMatrizView(View):
    def post(self, request, matriz_id):
        matriz = get_object_or_404(Matriz, id=matriz_id)
        user = request.user

        if user.is_superuser:
            matriz.delete()
            messages.success(request, 'La matriz ha sido eliminada directamente.')
            return redirect('matrices')

        changes = {
            'activo': {'old': matriz.activo, 'new': False},  # Simula desactivación
        }
        try:
            PendingChange.objects.create(
                model_name='matriz',
                object_id=matriz.id,
                changes=changes,
                submitted_by=user,
                action_type='delete'  # Indica que es una solicitud de eliminación
            )
            messages.success(request, 'El cambio de eliminación se ha registrado para revisión.')
        except Exception as e:
            messages.error(request, f'Error al registrar el cambio: {str(e)}')

        return redirect('matrices')


# Utils

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin, login_url='/login '), name='dispatch')
class PendingChangeApprovalView(View):
    def post(self, request, change_id):
        change = get_object_or_404(PendingChange, id=change_id)
        usuario = change.submitted_by  # Ya es una instancia de User
        action = request.POST.get("action")

        if action == "approve":
            # Obtener el modelo y la instancia correspondiente
            model = apps.get_model(app_label='core', model_name=change.model_name)
            instance = model.objects.get(pk=change.object_id)

            for field, values in change.changes.items():
                if "new" not in values:
                    messages.error(request, f"Error: No se encontró el valor 'new' para el campo {field}")
                    return redirect('cambios_pendientes')

                if field == "modified_by" or field == "submitted_by":
                    setattr(instance, field, usuario)
                elif field == "pais":
                    pais_instance = get_object_or_404(Pais, id=values["new"])
                    setattr(instance, field, pais_instance)
                else:
                    setattr(instance, field, values["new"])

            # Guardar la instancia
            instance.save()

            # Asegúrate de que el cambio pendiente sea aprobado inmediatamente
            change.approved = True
            change.save()

            # Refrescar la base de datos
            change.refresh_from_db()

            return redirect('cambios_pendientes')

        elif action == "reject":
            # Si se rechaza el cambio, no se realiza ninguna modificación en la instancia
            change.approved = False
            change.save()

        return redirect('cambios_pendientes')




# Vista genérica para capturar cambios en cualquier modelo
@method_decorator(login_required, name='dispatch')
class GuardarCambioGenerico(View):
    def post(self, request, model_name, object_id):
        """
        Guarda los cambios en cualquier modelo y crea un PendingChange.
        :param model_name: El nombre del modelo (como 'Matriz', 'Pais', etc.)
        :param object_id: El ID del objeto que está siendo editado.
        """
        model = apps.get_model('core', model_name)  # Obtener el modelo dinámicamente
        instance = get_object_or_404(model, pk=object_id)  # Obtener la instancia del objeto
        
        changes = {}  # Diccionario para almacenar los cambios
        
        # Iteramos sobre los campos del modelo y verificamos si hubo cambios
        for field in instance._meta.fields:
            field_name = field.name
            original_value = getattr(instance, field_name)
            new_value = request.POST.get(field_name)  # Suponiendo que el formulario envía los valores

            if str(original_value) != str(new_value):  # Si hay cambio
                changes[field_name] = {
                    'old': original_value,
                    'new': new_value
                }
        
        # Si hay cambios, creamos un PendingChange
        if changes:
            user = request.user  # El usuario que está haciendo el cambio
            PendingChange.objects.create(
                model_name=model_name,
                object_id=object_id,
                changes=changes,
                submitted_by=user  # Guardamos el usuario que realiza el cambio
            )
            messages.success(request, 'El cambio ha sido registrado correctamente.')
        else:
            messages.info(request, 'No se detectaron cambios.')

        return redirect('matrices')  # Redirige a donde quieras después de registrar el cambio

    
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
        