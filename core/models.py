from django.db import models
from django.contrib.auth.models import User

class Matriz(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    activo = models.CharField(max_length=3, choices=[('S', 'Sí'), ('N', 'No')], default='S')

class Broker(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/')  # El logo se almacena en la carpeta 'media/logos/'
    pais = models.CharField(max_length=100)
    domicilio_oficina = models.CharField(max_length=100)
    url_web = models.CharField(max_length=100)
    matriz = models.ForeignKey(Matriz, on_delete=models.CASCADE)
    activo = models.CharField(max_length=3, choices=[('S', 'Sí'), ('N', 'No')], default='S')

class Aseguradora(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=100)
    activo = models.CharField(max_length=3, choices=[('S', 'Sí'), ('N', 'No')], default='S')

