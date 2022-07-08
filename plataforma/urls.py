from django.urls import path
from . import views  # reconhecer onde está localizado a função paciente

# . = pasta atual, ou seja, da pasta plataforma


# passar todas as urls dentro da aplicação plataforma
# cada url é uma página html renderizada  
urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('dados_paciente/', views.dados_paciente_listar, name="dados_paciente_listar"),
    path('dados_paciente/<str:id>/', views.dados_paciente, name="dados_paciente"), # redireciona um id pela url a função da view
    path('grafico_peso/<str:id>/', views.grafico_peso, name="grafico_peso") # redireciona um id pela url a função da view
]
