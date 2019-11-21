from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import SearchForm
from .models import Products, Nutriments_for_100g, User_Favorites_Substitutes
from accounts.models import User
from .product_search import ProductSearch


def index(request):
    """Display the welcome page"""
    search_form = SearchForm()
    return render(request, 'store/index.html', {'search_form': search_form})


def products(request):
    """Search and display all product founded from user request"""
    search = ''
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search = search_form.cleaned_data.get('search_product')
            request.session['search'] = search

    elif 'search' in request.session:
        search = request.session['search']

    else:
        search_form = SearchForm()
        return render(request, 'store/products.html')

    products_list = Products.objects.filter(product_name__icontains=search).order_by('-nutrition_grade_fr')
    paginator = Paginator(products_list, 6)
    page = request.GET.get('page')
    try:
        products_found = paginator.get_page(page)
    except PageNotAnInteger:
        # If page not an Integer then deliver first page.
        products_found = paginator.get_page(1)
    except EmptyPage:
        # If page over the last result page, then deliver last result page.
        products_found = paginator.get_page(paginator.num_pages)
    context = {
        'search': search,
        'products_found': products_found,
        'paginate': True
    }

    return render(request, 'store/products.html', context)


def substitutes(request, product_id):
    """Found and display substitutes for a product"""
    init_product = Products.objects.get(pk=product_id)
    products_found = ProductSearch.found_substitutes(init_product.id)
    paginator = Paginator(products_found, 6)
    page = request.GET.get('page')
    try:
        products_found = paginator.page(page)
    except PageNotAnInteger:
        # If page not an Integer then deliver first page.
        products_found = paginator.page(1)
    except EmptyPage:
        # If page over the last result page, then deliver last result page.
        products_found = paginator.page(paginator.num_pages)
    context = {
        'init_product': init_product,
        'products_found': products_found,
        'paginate': True
    }

    return render(request, 'store/products.html', context)


def details(request, product_id):
    """Display de detail from a product or a substitute"""
    product_details = get_object_or_404(Products, pk=product_id)
    nutriments = Nutriments_for_100g.objects.filter(product__id=product_id).order_by('name')
    context = {
        'product_details': product_details,
        'nutriments': nutriments
    }
    return render(request, 'store/details.html', context)


@login_required(login_url='accounts:login')
def save_substitute(request, product_id, substitute_id):
    """Save a substitute to user favorites"""
    # if request.user.is_authenticated:
    user = User.objects.get(email=request.user)
    product = Products.objects.get(pk=product_id)
    substitute = Products.objects.get(pk=substitute_id)
    User_Favorites_Substitutes.objects.update_or_create(prod_base=product, prod_substitute=substitute, user=user)
    messages.success(request, 'Le substitut à été enregistré dans vos favoris')
    return redirect('store:substitutes', product_id)


@login_required(login_url='accounts:login')
def favorites_substitutes(request):
    favorites = User_Favorites_Substitutes.objects.filter(user=request.user)
    paginator = Paginator(favorites, 1)
    page = request.GET.get('page')
    try:
        products_list_p = paginator.page(page)
    except PageNotAnInteger:
        # If page not an Integer then deliver first page.
        products_list_p = paginator.page(1)
    except EmptyPage:
        # If page over the last result page, then deliver last result page.
        products_list_p = paginator.page(paginator.num_pages)

    context = {
        "products_list": products_list_p,
        'paginate': True
    }
    return render(request, 'store/favorites.html', context)

@login_required(login_url='accounts:login')
def delete_favorite(request, product_id, substitute_id):
    substitute = User_Favorites_Substitutes.objects.get(prod_base=product_id, prod_substitute=substitute_id, user=request.user)
    substitute.delete()
    messages.success(request, 'Le substitut à été supprimé')
    return redirect('store:favorites_substitutes')
