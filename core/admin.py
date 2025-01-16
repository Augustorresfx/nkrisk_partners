# admin.py
from django.contrib import admin
from .models import Matriz, PendingChange, Pais

# Registrar los modelos
admin.site.register(Matriz)
admin.site.register(PendingChange)
admin.site.register(Pais)
