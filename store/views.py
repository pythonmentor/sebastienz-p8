from django.shortcuts import render
from .forms import SearchForm

# Create your views here.

def index(request):
    search_form = SearchForm()
    return render(request, 'store/index.html', {'search_form':search_form})

# def login(request):
#     login_form = LoginForm()
#     return render(request, 'store/login.html', {'login_form':login_form})
#
# def register(request):
#     register_form = RegisterForm
#     return render(request, 'store/register.html', {'register_form':register_form})

def products(request):
    #form = search_form()
    return render(request, 'store/products.html')#, {'form':form})
