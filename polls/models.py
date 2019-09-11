import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Pregunta(models.Model):
    enunciado_pregunta = models.CharField(max_length=200)

    fecha_pub = models.DateTimeField('fecha de publicación')

    def __str__(self):
        #return str(self.id) + " - " + str(self.enunciado_pregunta)
        return str(self.enunciado_pregunta)

    def fue_publicada_recientemente(self):
        ahora = timezone.now()
        return ahora - datetime.timedelta(days=1) <= self.fecha_pub <= ahora

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    texto_opcion = models.CharField(max_length=200)

    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.texto_opcion
