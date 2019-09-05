from django.http import Http404
from django.shortcuts import get_object_or_404, render

#Borrar httpresponse y loader cuando se cambien todos los métodos para que usen render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.urls import reverse

from .models import Pregunta, Opcion


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

    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)

    try:
        opcion_seleccionada = pregunta.opcion_set.get(pk=request.POST['opcion'])
    except (KeyError, Pregunta.DoesNotExist):

        #vuelve a cargar la pregunta si hay un error asignando la opción
        return render(request, 'polls/detalle.html', {
            'pregunta': pregunta,
            'mensaje_error': "No se ha seleccionado ninguna opción",
        })
    else:
        opcion_seleccionada.votos +=1
        opcion_seleccionada.save()
        return HttpResponseRedirect(reverse('polls:resultados', args=(pregunta.id,)))
