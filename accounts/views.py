from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .forms import LoginForm, RegisterForm

from django.contrib import messages


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            raw_password = login_form.cleaned_data.get('password')
            authenticate_user = authenticate(username=username, password=raw_password)
            if authenticate_user is not None:
                login(request, authenticate_user)
                return HttpResponseRedirect('/')
            else:
                register_form = RegisterForm()
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
            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            authenticate_user = authenticate(username=username, password=raw_password)
            login(request, authenticate_user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'accounts/register.html', {'register_form': register_form})
    else:
        register_form = RegisterForm()
        return render(request, 'accounts/register.html', {'register_form': register_form})


def get_logged_customer_from_request(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        if len(Customer.objects.filter(id=logged_user_id)) == 1:
            return Customer.objects.filter(id=logged_user_id)[0]
        else:
            return ''
    else:
        return None
