from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from .forms import LoginForm, RegisterForm, AccountForm
from .models import User

from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            authenticate_user = authenticate(email=email, password=password)
            if authenticate_user is not None:
                login(request, authenticate_user)
                messages.success(request, "Vous êtes maintenant connecté à votre compte")
                return HttpResponseRedirect('/')
            else:
                messages.error(request, "Email ou mot de passe invalide !")
                return render(request, 'accounts/login.html', {'login_form': login_form})
        else:
            login_form = LoginForm()
            return render(request, 'accounts/login.html', {'login_form': login_form})

    login_form = LoginForm()
    return render(request, 'accounts/login.html', {'login_form': login_form})


def user_logout(request):
    logout(request)
    messages.info(request, 'Vous êtes déconnecté !')
    return HttpResponseRedirect('/')


def user_register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save(commit=True)
            email = register_form.cleaned_data.get('email')
            password1 = register_form.cleaned_data.get('password1')
            authenticate_user = authenticate(email=email, password=password1)
            login(request, authenticate_user)
            messages.success(request, "Votre compte à été créé avec succès et vous êtes connecté !")
            return HttpResponseRedirect('/')
        else:
            return render(request, 'accounts/register.html', {'register_form': register_form})
    else:
        register_form = RegisterForm()
        return render(request, 'accounts/register.html', {'register_form': register_form})


@login_required(login_url='accounts:login')
def user_account(request):
    current_user = User.objects.get(pk=request.user.id)
    if request.method == "POST":
        account_form = AccountForm(request.POST, instance=current_user)
        if account_form.is_valid():
            account_form.save()
            return HttpResponseRedirect(reverse('accounts:myaccount'))
        else:
            return render(request, 'accounts/myaccount.html', {'account_form': account_form})
    else:
        account_form = AccountForm(instance=current_user)
        return render(request, 'accounts/myaccount.html', {'account_form': account_form})

