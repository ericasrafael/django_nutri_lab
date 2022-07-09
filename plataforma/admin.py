from django.contrib import admin
from .models import Pacientes, DadosPaciente, Refeicao, Opcao


# cadastrar tabelas na área administrativa do django 

admin.site.register(Pacientes)
admin.site.register(DadosPaciente)
admin.site.register(Refeicao)
admin.site.register(Opcao)
