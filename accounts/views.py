import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, AccountForm

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
            return HttpResponseRedirect('/')
        else:
            return render(request, 'accounts/register.html', {'register_form': register_form})
    else:
        register_form = RegisterForm()
        return render(request, 'accounts/register.html', {'register_form': register_form})


@login_required(login_url='accounts:login')
def user_account(request):
    account_form = AccountForm(instance=request.user)
    return render(request, 'accounts/myaccount.html', {'account_form': account_form})


@login_required(login_url='accounts:login')
def user_products(request):
    pass
