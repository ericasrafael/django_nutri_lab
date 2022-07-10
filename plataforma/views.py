from email.policy import HTTP
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Pacientes, DadosPaciente, Refeicao, Opcao
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# funções requisitadas por cada url


# função abaixo só poderá ser acessada por usuários logados
@login_required(login_url='/auth/logar/')
# Renderizando cada requisição (url da aplicação)
def pacientes(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html', {'pacientes': pacientes})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR,
                                 'Preencha todos os campos!')
            return redirect('/pacientes/')
        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR,
                                 'Digite uma idade válida')
            return redirect('/pacientes/')

        pacientes = Pacientes.objects.filter(email=email)

        if pacientes.exists():
            messages.add_message(request, constants.ERROR,
                                 'Já existe um paciente com esse E-mail!')
            return redirect('/pacientes/')

        try:
            paciente = Pacientes(nome=nome,
                                 sexo=sexo,
                                 idade=idade,
                                 email=email,
                                 telefone=telefone,
                                 nutri=request.user)  # retorna usuário que está logado
            paciente.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Paciênte cadastrado com sucesso!')
            return redirect('/pacientes/')
        except:
            messages.add_message(request, constants.ERROR,
                                 'Erro interno do sistema!')
            return redirect('/pacientes/')


@login_required(login_url='/auth/logar/')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        # enviar pro html os pacientes
        return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes})


@login_required(login_url='/auth/logar/')
def dados_paciente(request, id):  # recebe id da url (urls)
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR,
                             'Esse paciente não é seu!')
        return redirect('/dados_paciente/')
    if request.method == "GET":
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})
    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        # name das tags input de dados_paciente
        gordura = request.POST.get('gordura')
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
        messages.add_message(request, constants.SUCCESS,
                             'Dados cadastrado com sucesso!')
        return redirect('/dados_paciente/')


@login_required(login_url='/auth/logar/')
@csrf_exempt
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by(
        "data")  # dados do paciente do id=id, ordenados pela data

    # dos dados obtidos, retorne somente o peso dentro da lista
    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos,     # eixo y
            'labels': labels}  # eixo x
    return JsonResponse(data)


def plano_alimentar_listar(request):
    if request.method == "GET":
        # lista pacientes filtrando os pacientes do nitricionista logado
        pacientes = Pacientes.objects.filter(nutri=request.user)
        # envia os dados para o html
        return render(request, 'plano_alimentar_listar.html', {'pacientes': pacientes})


def plano_alimentar(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        # Se paciente não for do nutricionista cadastrado, mostre a mensagem de erro e retorne a dados dos pacientes
        messages.add_message(request, constants.ERROR,
                             'Esse paciente não é seu')
        return redirect('/plano_alimentar_listar/')
    if request.method == "GET":

        # filtrando as refeições cadastradas apenas do paciente analisado
        r1 = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        opcao = Opcao.objects.all()
        # repassa o paciente e suas informações para o html
        return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao': r1,'opcao':opcao})


def refeicao(request, id_paciente):
    # armazena paciente cujo id está na url passada
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:  # verifica se o paciente é do nutricionista logado
        messages.add_message(request, constants.ERROR,
                             'Esse paciente não é seu')
        return redirect('/dados_paciente/')
    if request.method == "POST":  # requisição que veio pelo formulário, capture os dados em variaveis
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        # exatamente como tá em "name" na tag
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        r1 = Refeicao(paciente=paciente,
                      titulo=titulo,
                      horario=horario,
                      carboidratos=carboidratos,
                      proteinas=proteinas,
                      gorduras=gorduras)
        r1.save()  # salva no banco de dados, na tabela Refeicao
        messages.add_message(request, constants.SUCCESS,
                             'Refeição cadastrada!')
        # redireciona pro paciente
        return redirect(f'/plano_alimentar/{id_paciente}')


def opcao(request, id_paciente):
    if request.method == "POST":
        # armazenando as informações do formulário
        id_refeicao = request.POST.get('refeicao')
        # files recebem arquivos: pdf, imagens, vídeos, etc. OBS: enctype='multipart/form-data' deve está na tag html para enviar os arquivos para o back-end
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get("descricao")

        # instanciando na função de armazenamento no BD
        o1 = Opcao(refeicao_id=id_refeicao,
                   imagem=imagem,
                   descricao=descricao)

        # Salvando no BD
        o1.save()

        messages.add_message(request, constants.SUCCESS, 'Opcao cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')
