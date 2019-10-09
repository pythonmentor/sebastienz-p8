from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .forms import SearchForm
from accounts import views as accounts_views

# Create your views here.

def index(request):
    search_form = SearchForm()
    logged_customer = accounts_views.get_logged_customer_from_request(request)
    context = {
        'search_form':search_form,
        'logged_customer':logged_customer
    }
    return render(request, 'store/index.html', context)

def products(request):
    #form = search_form()
    return render(request, 'store/products.html')#, {'form':form})
