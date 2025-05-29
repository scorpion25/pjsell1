from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadExcelForm
import pandas as pd
from django.utils.timezone import localtime
from .models import Contato, Configuracao, RelatorioEnvio
from django.utils import timezone
from datetime import datetime
import threading
import requests
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import os

def enviar_mensagem_se_nao_cancelado(relatorio_id, texto, url, headers):
    try:
        agendamento = RelatorioEnvio.objects.get(id=relatorio_id)
        if agendamento.cancelado:
            print(f"❌ Envio cancelado para {agendamento.numero}")
            return

        payload = {
            "phone": agendamento.numero,
            "message": texto
        }
        response = requests.post(url, json=payload, headers=headers)
        print(f"✅ Enviado para {agendamento.numero} | Status: {response.status_code}")
    except RelatorioEnvio.DoesNotExist:
        print("⚠️ Agendamento não encontrado.")


def agendar_envio_mensagens(contatos, mensagens, usuario):
    url = "https://api.z-api.io/instances/3E1664822BF440DCF6C9FE99C2B48794/token/3E6D6FDD5AF8252B380DACA8/send-text"
    headers = {
        "Content-Type": "application/json",
        "Client-Token": "F466390c69345429ba80cec680a7f5987S"
    }

    for contato in contatos:
        data_m1 = timezone.now()
        data_m2 = None
        data_m3 = None

        for msg in mensagens:
            if msg['tipo'] == 'Mensagem 2':
                data_m2 = f"{msg['data']} {msg['hora']}"
            if msg['tipo'] == 'Mensagem 3':
                data_m3 = f"{msg['data']} {msg['hora']}"

        relatorio = RelatorioEnvio.objects.create(
            numero=contato.numero,
            pon=contato.pon,
            data_m1=data_m1,
            data_m2=data_m2,
            data_m3=data_m3,
            funcionario=usuario,
            cancelado=False
        )

        for msg in mensagens:
            if not msg['mensagem'] or not msg['data'] or not msg['hora']:
                continue

            agendamento_str = f"{msg['data']} {msg['hora']}"
            agendamento_dt = datetime.strptime(agendamento_str, "%Y-%m-%d %H:%M")
            agora = timezone.localtime().replace(tzinfo=None)

            delay = (agendamento_dt - agora).total_seconds()
            if delay > 0:
                threading.Timer(delay, enviar_mensagem_se_nao_cancelado, args=(relatorio.id, msg['mensagem'], url, headers)).start()
            else:
                print(f"⚠️ Horário passado para {msg['tipo']}, envio ignorado.")

@staff_member_required
def painel_superusuario(request):
    return render(request, 'pjsell/painel_superusuario.html')


@login_required
def enviar(request):
    config, _ = Configuracao.objects.get_or_create(id=1)
    contatos_filtrados = []
    mensagem_sucesso = None
    mensagem_erro = None

    if request.method == 'POST':
        data_lista = request.POST.get('data_envio')

        if data_lista:
            contatos_filtrados = Contato.objects.filter(data_m1__date=data_lista)

        mensagens_a_enviar = []

        if 'enviar_msg1' in request.POST:
            mensagens_a_enviar.append({
                'mensagem': config.mensagem_1,
                'data': request.POST.get('data_msg1'),
                'hora': request.POST.get('hora_msg1'),
                'tipo': 'Mensagem 1'
            })

        if 'enviar_msg2' in request.POST:
            mensagens_a_enviar.append({
                'mensagem': config.mensagem_2,
                'data': request.POST.get('data_msg2'),
                'hora': request.POST.get('hora_msg2'),
                'tipo': 'Mensagem 2'
            })

        if 'enviar_msg3' in request.POST:
            mensagens_a_enviar.append({
                'mensagem': config.mensagem_3,
                'data': request.POST.get('data_msg3'),
                'hora': request.POST.get('hora_msg3'),
                'tipo': 'Mensagem 3'
            })

        if not mensagens_a_enviar:
            mensagem_erro = "⚠️ Selecione pelo menos uma mensagem e preencha data e hora."
        else:
            agendar_envio_mensagens(contatos_filtrados, mensagens_a_enviar, request.user)
            mensagem_sucesso = "✅ Mensagens agendadas com sucesso."

        return render(request, 'pjsell/enviar.html', {
            'config': config,
            'contatos': contatos_filtrados,
            'mensagens_enviadas': mensagens_a_enviar,
            'mensagem_sucesso': mensagem_sucesso,
            'mensagem_erro': mensagem_erro
        })

    return render(request, 'pjsell/enviar.html', {
        'config': config,
        'contatos': contatos_filtrados
    })


@login_required
def resumo_config(request):
    config, created = Configuracao.objects.get_or_create(id=1)
    return render(request, 'pjsell/resumo.html', {'config': config})


@login_required
def historico(request):
    data_filtrada = request.GET.get('data')
    contatos = Contato.objects.all()

    if data_filtrada:
        try:
            data_formatada = datetime.strptime(data_filtrada, '%Y-%m-%d').date()
            contatos = contatos.filter(data_m1__date=data_formatada)
        except ValueError:
            pass

    contatos = contatos.order_by('-data_m1')

    return render(request, 'pjsell/historico.html', {
        'contatos': contatos,
        'data_selecionada': data_filtrada
    })


@login_required
def pesquisar(request):
    termo = request.GET.get('q')
    resultado = []

    if termo:
        resultado = Contato.objects.filter(Q(numero__icontains=termo) | Q(pon__icontains=termo))

    return render(request, 'pjsell/pesquisar.html', {
        'termo': termo,
        'resultado': resultado
    })


@login_required
def definicoes(request):
    config, created = Configuracao.objects.get_or_create(id=1)

    if request.method == 'POST':
        config.mensagem_1 = request.POST.get('mensagem_1')
        config.mensagem_2 = request.POST.get('mensagem_2')
        config.mensagem_3 = request.POST.get('mensagem_3')
        config.save()
        return redirect('definicoes')

    return render(request, 'pjsell/definicoes.html', {'config': config})


@login_required
def painel(request):
    return render(request, 'pjsell/painel.html', {'usuario': request.user})


@login_required
def new_send(request):
    contexto = {}

    if request.method == 'POST' and request.FILES.get('arquivo'):
        excel_file = request.FILES['arquivo']
        nome_arquivo = os.path.basename(excel_file.name)

        try:
            df = pd.read_excel(excel_file, header=None)

            if df.shape[1] != 2:
                contexto['erro'] = '⚠️ O arquivo deve conter exatamente 2 colunas.'
            else:
                for index, row in df.iterrows():
                    Contato.objects.create(
                        numero=row[0],
                        pon=row[1],
                        funcionario=request.user
                    )
                contexto['sucesso'] = '✅ Contatos importados com sucesso!'
                contexto['nome_arquivo'] = nome_arquivo

        except Exception as e:
            contexto['erro'] = f'❌ Erro ao processar o arquivo: {e}'
            contexto['nome_arquivo'] = nome_arquivo

    return render(request, 'pjsell/new_send.html', contexto)


@login_required
def relatorio(request):
    data_filtro = request.GET.get('data')
    relatorios = RelatorioEnvio.objects.all()

    if data_filtro:
        try:
            data_formatada = datetime.strptime(data_filtro, "%Y-%m-%d").date()
            relatorios = relatorios.filter(data_m1__date=data_formatada)
        except ValueError:
            pass

    return render(request, 'pjsell/relatorio.html', {
        'relatorios': relatorios,
        'data_selecionada': data_filtro
    })


@login_required
def cancelar_agendamento(request, relatorio_id):
    try:
        agendamento = RelatorioEnvio.objects.get(id=relatorio_id)
        agendamento.cancelado = True
        agendamento.save()
        return redirect('relatorio')
    except RelatorioEnvio.DoesNotExist:
        return redirect('relatorio')
