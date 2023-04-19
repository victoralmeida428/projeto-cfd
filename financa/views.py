from django.shortcuts import render
from financa.formularios.forms import *
from django.contrib import auth, messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from financa.models import BancoUsuarios

def index(request):
    return render(request, 'financa/index.html')

def cadastro_efetuado(request):
    messages.success(request, 'Cadastrado com sucesso')
    return render(request, 'financa/cadastro_efetuado.html')

def login(request):   
    if request.method == 'GET':
        form = Login()
        context = {
            'form': form
        }
        
        return render(request, 'financa/login.html', context)
    else:
        form = Login(request.POST)
        
        if form.is_valid():
            login = form.cleaned_data['login']
            senha = BancoUsuarios.objects.filter(login=login).values()

            usuario = auth.authenticate(
                request,
                username=login,
                password=senha[0]['senha']
            )
            auth.login(request, usuario)
            messages.success(request, f'{login} Logado com sucesso')            
            return redirect('index')
        context = {
                'form': form
            }

        return render(request, 'financa/login.html', context=context)

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso')
    return redirect('login')

def cadastro(request):
    if request.method == 'GET':
        form = RegistroSite()
        context = {
            'form': form
        }
        return render(request, 'financa/cadastro.html', context=context)
    else:
        cliente = ClienteForm(request.POST)
        form = RegistroSite(request.POST)

        
        if form.is_valid():
            cliente.save()
            context = {
                'form': form
            }
            login = cliente.cleaned_data.get('login')
            senha = cliente.cleaned_data.get('senha')
            email = cliente.cleaned_data.get('email')
            print(login, senha, email)
            usuario = User.objects.create_user(
                username=login,
                password=senha,
                email=email
            )
            usuario.save()

            return redirect('cadastro_efetuado')

            
        
        context = {
                'form': form
            }

        return render(request, 'financa/cadastro.html', context=context)
        

    
def about(request):
    return render(request, 'financa/about.html')


