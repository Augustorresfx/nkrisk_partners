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
from .views import SignInView, SignOutView, HomeView, InicioView

handler404 = pagina_no_encontrada

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', SignInView.as_view(), name="login"),
    path('logout/', SignOutView.as_view(), name="logout"),
    path('', HomeView.as_view(), name='home'),
    path('inicio/', InicioView.as_view(), name='inicio'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
