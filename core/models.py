from django.db import models
from django.contrib.auth.models import User

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)  # Código ISO 3166-1 alpha-3

    def __str__(self):
        return self.nombre

class PendingChange (models.Model):
    model_name = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()  # ID del objeto modificado
    changes = models.JSONField()  # Guarda los cambios en formato JSON
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_changes")
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=None, null=True)  # None = Pendiente, True/False = Aprobado/Rechazado

    def __str__(self):
        return f"Cambio en {self.model_name} por {self.submitted_by.username}"

class Matriz(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:  # Solo para objetos existentes
            # Obtener el estado actual del objeto
            original = Matriz.objects.get(pk=self.pk)
            changes = {}
            for field in self._meta.fields:
                field_name = field.name
                original_value = getattr(original, field_name)
                new_value = getattr(self, field_name)
                if original_value != new_value:
                    changes[field_name] = {"antiguo": original_value, "nuevo": new_value}

            # Guardar los cambios pendientes si existen
            if changes:
                from .models import PendingChange
                PendingChange.objects.create(
                    model_name=self._meta.model_name,
                    object_id=self.pk,
                    changes=changes,
                    submitted_by=self.modified_by,
                )
        else:
            # Para objetos nuevos, guardarlos directamente
            super().save(*args, **kwargs)

class Broker(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/')  # El logo se almacena en la carpeta 'media/logos/'
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    domicilio_oficina = models.CharField(max_length=100)
    url_web = models.CharField(max_length=100)
    matriz = models.ForeignKey(Matriz, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

class Aseguradora(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    tax_id = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

