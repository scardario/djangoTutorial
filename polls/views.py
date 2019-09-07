from django.http import Http404
from django.shortcuts import get_object_or_404, render

#Borrar httpresponse y loader cuando se cambien todos los métodos para que usen render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.urls import reverse
from django.views import generic

from .models import Pregunta, Opcion


class vistaIndex(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lista_preguntas_actualizada'

    def get_queryset(self):
        return Pregunta.objects.order_by('-fecha_pub')[:5]

class vistaDetalle(generic.DetailView):
    model = Pregunta
    template_name = 'polls/detalle.html'

class vistaResultados(generic.DetailView):
    model = Pregunta
    template_name = 'polls/resultados.html'

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
