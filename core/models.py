from django.db import models
from django.contrib.auth.models import User

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)  # Código ISO 3166-1 alpha-3

    def __str__(self):
        return self.nombre

class Matriz(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    activo = models.CharField(max_length=10, choices=[('S', 'Sí'), ('N', 'No')], default='S')

class Broker(models.Model):
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/')  # El logo se almacena en la carpeta 'media/logos/'
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    domicilio_oficina = models.CharField(max_length=100)
    url_web = models.CharField(max_length=100)
    matriz = models.ForeignKey(Matriz, on_delete=models.CASCADE)
    activo = models.CharField(max_length=10, choices=[('S', 'Sí'), ('N', 'No')], default='S')

class Aseguradora(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    tax_id = models.CharField(max_length=100)
    activo = models.CharField(max_length=10, choices=[('S', 'Sí'), ('N', 'No')], default='S')

