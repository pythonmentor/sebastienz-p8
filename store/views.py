from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .forms import SearchForm
from accounts import views as accounts_views

# Create your views here.

def index(request):
    search_form = SearchForm()

    context = {
        'search_form':search_form,

    }
    return render(request, 'store/index.html', context)

def products(request):
    #form = search_form()
    return render(request, 'store/products.html')#, {'form':form})
