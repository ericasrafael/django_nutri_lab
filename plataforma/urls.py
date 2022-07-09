from django.urls import path
from . import views  # reconhecer onde está localizado a função paciente

# . = pasta atual, ou seja, da pasta plataforma


# passar todas as urls dentro da aplicação plataforma
# cada url é uma página html renderizada  
urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('dados_paciente/', views.dados_paciente_listar, name="dados_paciente_listar"),
    path('dados_paciente/<str:id>/', views.dados_paciente, name="dados_paciente"), # redireciona um id pela url a função da view
    path('grafico_peso/<str:id>/', views.grafico_peso, name="grafico_peso"), # redireciona um id pela url a função da view
    path('plano_alimentar_listar/', views.plano_alimentar_listar, name="plano_alimentar_listar"),
    path('plano_alimentar/<str:id>/', views.plano_alimentar, name="plano_alimentar"),
    path('refeicao/<str:id_paciente>/', views.refeicao, name="refeicao"),  # redireciona dados das refeições para a model refeição
]
