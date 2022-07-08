from email.policy import HTTP
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Pacientes, DadosPaciente
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# funções requisitadas por cada url


@login_required(login_url='/auth/logar/') # função abaixo só poderá ser acessada por usuários logados
# Renderizando cada requisição (url da aplicação)
def pacientes(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html',{'pacientes':pacientes})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
            return redirect('/pacientes/')
        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
            return redirect('/pacientes/')
        
        pacientes = Pacientes.objects.filter(email=email)
        
        if pacientes.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail!')
            return redirect('/pacientes/')
        
        
        try:
                paciente = Pacientes(nome=nome,
                                sexo=sexo,
                                idade=idade,
                                email=email,
                                telefone=telefone,
                                nutri=request.user)  # retorna usuário que está logado

                paciente.save()

                messages.add_message(request, constants.SUCCESS, 'Paciênte cadastrado com sucesso!')
                return redirect('/pacientes/')
        except:
                messages.add_message(request, constants.ERROR, 'Erro interno do sistema!')
                return redirect('/pacientes/')
            
@login_required(login_url='/auth/logar/')

def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes}) # enviar pro html os pacientes
                                                            
                                                                                                                      
@login_required(login_url='/auth/logar/')

def dados_paciente(request, id):  # recebe id da url (urls)
    paciente = get_object_or_404(Pacientes, id=id)
    
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu!')
        return redirect('/dados_paciente/')
        
    if request.method == "GET":
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})
    
    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')  # name das tags input de dados_paciente
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')
        
        paciente = DadosPaciente(paciente=paciente,   # paciente retornado da tabela Pacientes
                                data=datetime.now(),  # data atual
                                peso=peso,
                                altura=altura,
                                percentual_gordura=gordura,
                                percentual_musculo=musculo,
                                colesterol_hdl=hdl,
                                colesterol_ldl=ldl,
                                colesterol_total=colesterol_total,
                                trigliceridios=triglicerídios)

        paciente.save()

        messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso!')

        return redirect('/dados_paciente/')
    
    
    

@login_required(login_url='/auth/logar/')
@csrf_exempt

def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by("data") # dados do paciente do id=id, ordenados pela data
    
    pesos = [dado.peso for dado in dados] # dos dados obtidos, retorne somente o peso dentro da lista
    labels = list(range(len(pesos)))
    data = {'peso': pesos,     # eixo y
            'labels': labels}  # eixo x
    return JsonResponse(data)