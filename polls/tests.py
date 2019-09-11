import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Pregunta

def crear_pregunta(enunciado_pregunta, dias):
    """crear una pregunta a ser publicada en cierta cantidad de días - negativo
    para crear preguntas publicadas en el pasado"""
    fecha = timezone.now() + datetime.timedelta(days=dias)
    return Pregunta.objects.create(enunciado_pregunta=enunciado_pregunta, fecha_pub=fecha)

# Create your tests here.

class pruebasPreguntaVistaDetalle(TestCase):
    def test_pregunta_futuro(self):
        #la vista detalle de una pregunta con fecha_pub en el futuro debería devolver un 404
        pregunta_futuro = crear_pregunta(enunciado_pregunta="Pregunta futuro", dias=5)
        url = reverse('polls:detalle', args=(pregunta_futuro.id,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_pregunta_pasado(self):
        #la vista detalle muestra el texto de la pregunta
        pregunta_pasado = crear_pregunta(enunciado_pregunta="Pregunta pasado", dias=-5)
        url = reverse('polls:detalle', args=(pregunta_pasado.id,))
        resp = self.client.get(url)
        self.assertContains(resp, pregunta_pasado.enunciado_pregunta)

class pruebasPreguntaVistaIndex(TestCase):

    def test_no_preguntas(self):
        #si no hay preguntas, debería haber un mensaje apropiado
        resp = self.client.get(reverse('polls:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'No hay preguntas disponibles.')
        self.assertQuerysetEqual(resp.context['lista_preguntas_actualizada'], [])

    def test_preguntas_pasado(self):
        #preguntas con fecha_pub de fecha pasada son publicadas en el index
        crear_pregunta(enunciado_pregunta="Pregunta pasado.", dias=-30)
        resp = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            resp.context['lista_preguntas_actualizada'],
            ['<Pregunta: Pregunta pasado.>']
        )

    def test_preguntas_futuro(self):
        #Preguntas con fecha en el futuro no son publicadas en el index
        crear_pregunta(enunciado_pregunta="Pregunta futuro.", dias=30)
        resp = self.client.get(reverse('polls:index'))
        self.assertContains(resp, "No hay preguntas disponibles.")
        self.assertQuerysetEqual(resp.context['lista_preguntas_actualizada'], [])

    def test_preguntas_pasado_futuro(self):
        #Aún cuando existen ambos tipos, solo se muestra la del pasado
        crear_pregunta(enunciado_pregunta="Pregunta pasado.", dias=-30)
        crear_pregunta(enunciado_pregunta="Pregunta futuro.", dias=30)
        resp = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            resp.context['lista_preguntas_actualizada'],
            ['<Pregunta: Pregunta pasado.>']
        )

    def test_dos_preguntas_pasado(self):
        crear_pregunta(enunciado_pregunta="Pregunta pasado 1.", dias=-30)
        crear_pregunta(enunciado_pregunta="Pregunta pasado 2.", dias=-5)
        resp = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            resp.context['lista_preguntas_actualizada'],
            ['<Pregunta: Pregunta pasado 2.>', '<Pregunta: Pregunta pasado 1.>']
        )


class pruebasModeloPregunta(TestCase):

    def test_publicada_recientemente_pregunta_futura(self):
        fecha = timezone.now() + datetime.timedelta(days=30)
        pregunta_futura = Pregunta(fecha_pub=fecha)
        self.assertIs(pregunta_futura.fue_publicada_recientemente(), False)


    def test_publicada_recientemente_pregunta_vieja(self):
        """fue_publicada_recientemente() devuelve False para preguntas que tengan más
        de 1 día
        """
        fecha = timezone.now() + datetime.timedelta(days=1, seconds=1)
        pregunta_vieja = Pregunta(fecha_pub=fecha)
        self.assertIs(pregunta_vieja.fue_publicada_recientemente(), False)

    def test_publicada_reciemente_pregunta_reciente(self):
        """fue_publicada_recientemente() devuelve True para preguntas que hayan sido
        publicadas durante el último día
        """
        fecha = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pregunta_reciente = Pregunta(fecha_pub=fecha)
        self.assertIs(pregunta_reciente.fue_publicada_recientemente(), True)

