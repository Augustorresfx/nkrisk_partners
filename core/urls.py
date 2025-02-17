"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import pagina_no_encontrada
from django.conf.urls import handler404
from django.conf import settings
from .views import SignInView, SignOutView, HomeView, InicioView, MatrizView, EliminarMatrizView, EditarMatrizView, CambiosPendientesView, PendingChangeApprovalView, GuardarCambioGenerico

handler404 = pagina_no_encontrada

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', SignInView.as_view(), name="login"),
    path('logout/', SignOutView.as_view(), name="logout"),
    path('', HomeView.as_view(), name='home'),
    path('inicio/', InicioView.as_view(), name='inicio'),

    # MATRICES
    path('matrices/', MatrizView.as_view(), name="matrices"),
    path('matrices/<int:matriz_id>/eliminar/', EliminarMatrizView.as_view(), name='delete_matriz'),
    path('matrices/<int:matriz_id>/editar/', EditarMatrizView.as_view(), name='update_matriz'),

    # CAMBIOS PENDIENTES
    path('cambios_pendientes/', CambiosPendientesView.as_view(), name='cambios_pendientes'),
    path('approve-change/<int:change_id>/', PendingChangeApprovalView.as_view(), name='approve_change'),
    path('guardar-cambio/<str:model_name>/<int:object_id>/', GuardarCambioGenerico.as_view(), name='guardar_cambio'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
