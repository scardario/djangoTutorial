from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    #/polls/
    path('', views.index, name='index'),
    # /polls/5/
    path('<int:pregunta_id>/', views.detalle, name='detalle'),
    # /polls/5/resultados/
    path('<int:pregunta_id>/resultados/', views.resultados, name='resultados'),
    # /polls/5/votacion/
    path('<int:pregunta_id>/votacion/', views.votacion, name='votacion'),
]
