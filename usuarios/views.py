from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro.html', {'error_username': 'Usuário já cadastrado!'})

        if User.objects.filter(email=email).exists():
            return render(request, 'cadastro.html', {'error_email': 'Este email já está cadastrado!'})

        if len(senha) < 6:
            return render(request, 'cadastro.html', {'error_senha': 'A senha deve ter pelo menos 6 caracteres.'})

        User.objects.create_user(username=username, email=email, password=senha)
        return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # ✅ Corrigido aqui
            if user.is_superuser:
                return redirect('painel_superusuario')
            else:
                return redirect('painel')
    else:
        form = AuthenticationForm()
    return render(request, 'pjsell/login.html', {'form': form})
