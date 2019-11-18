from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from .forms import SearchForm
from .models import Products, Nutriments_for_100g
from .product_search import ProductSearch


def index(request):
    search_form = SearchForm()
    return render(request, 'store/index.html', {'search_form': search_form})


def products(request):
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
    product = Products.objects.get(pk=product_id)
    products_found = ProductSearch.found_substitutes(product.id)
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
        'product': product,
        'products_found': products_found,
        'paginate': True
    }

    return render(request, 'store/products.html', context)


def details(request, product_id):
    product_details = get_object_or_404(Products, pk=product_id)
    nutriments = Nutriments_for_100g.objects.filter(product__id=product_id).order_by('name')
    context = {
        'product_details': product_details,
        'nutriments': nutriments
    }
    return render(request, 'store/details.html', context)

