from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.

# def index(request):
#     return redirect('/agenda/') #redireciona para agenda

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST: #Quando for do tipo POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username,
                               password=password) #Faz a verificação, se o login e senha estão corretos
        if usuario is not None: #Se existir o Usuário e a senha
            login(request, usuario) #Faz o login do usuário
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha inválido')
    return redirect('/')

@login_required(login_url='/login/') #Só abre se tiver um login, se não incontrar ele leva para a url ./login/
def lista_eventos(request):
    usuario = request.user #usuário de quem da requisitando
    data_atual = datetime.now() - timedelta(hours=1)
    # evento = Evento.objects.get(id=1) #pega o primeiro evento criado
    # evento = Evento.objects.all() #Pega todos os eventos criados

    evento = Evento.objects.filter(usuario=usuario, #filtra para aparecer os eventos apenas do usuário que está logado
                                   data_evento__gt=data_atual)  #__gt é, se data atual for maior que data_evento, ele retorna, se colocat __lt, serão os menores
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def eventos(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                            descricao=descricao,
            #                                            data_evento=data_evento)
            evento = Evento.objects.get(id=id_evento) #Outra forma de fazer as alterações
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save() #Comita as mudanças
        else:
            Evento.objects.create(titulo=titulo,
                                  descricao=descricao,
                                  data_evento=data_evento,
                                  usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404() #Mostra um erro de not found
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario,).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False) #Retorna em forma json