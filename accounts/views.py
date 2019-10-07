from django.shortcuts import render
from .forms import LoginForm, RegisterForm

# Create your views here.

def login(request):
    login_form = LoginForm()
    return render(request, 'accounts/login.html', {'login_form':login_form})

def register(request):
    register_form = RegisterForm
    return render(request, 'accounts/register.html', {'register_form':register_form})
