from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    #/polls/
    path('', views.vistaIndex.as_view(), name='index'),
    # /polls/5/
    path('<int:pk>/', views.vistaDetalle.as_view(), name='detalle'),
    # /polls/5/resultados/
    path('<int:pk>/resultados/', views.vistaResultados.as_view() , name='resultados'),
    # /polls/5/votacion/
    path('<int:pregunta_id>/votacion/', views.votacion, name='votacion'),
]
