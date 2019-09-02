from django.http import Http404
from django.shortcuts import get_object_or_404, render

#Borrar estos dos cuando se cambien todos los métodos para que usen render
from django.http import HttpResponse
from django.template import loader

from .models import Pregunta


def index(request):
    lista_preguntas_actualizada = Pregunta.objects.order_by('-fecha_pub')[:5]
    contexto = {
        'lista_preguntas_actualizada': lista_preguntas_actualizada,
    }
    return render(request, 'polls/index.html', contexto)

def detalle(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, "polls/detalle.html", {'pregunta': pregunta})

def resultados(request, pregunta_id):
    respuesta = "Está consultando los resultados de la pregunta %s."
    return HttpResponse(respuesta % pregunta_id)

def votacion(request, pregunta_id):
    return HttpResponse("Está votando en la pregunta %s." % pregunta_id)
