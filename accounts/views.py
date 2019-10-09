from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from .models import Customer

# Create your views here.

def login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.filter(email = email)
        if not customer.exists():
            register_form  = RegisterForm()
            return render(request, 'accounts/register.html', {'register_form':register_form})
        else:
            request.session['logged_customer_id'] = customer.id
            HttpResponseRedirect('/')
    return render(request, 'accounts/login.html', {'login_form':login_form})

def logout(request):
    try:
        del request.session['logged_customer']
    except KeyError:
        pass
    return HttpResponseRedirect('/')

def register(request):
    register_form = RegisterForm
    if request.method == 'POST':
        pseudo= register_form.cleaned_data['pseudo']
        last_name= register_form.cleaned_data['last_name']
        first_name= register_form.cleaned_data['first_name']
        email= register_form.cleaned_data['email']
        password= register_form.cleaned_data['password']
    return render(request, 'accounts/register.html', {'register_form':register_form})

def get_logged_customer_from_request(request):
    if 'logged_customer_id' in request.session:
        logged_customer_id = request.session['logged_customer_id']
        if len(Customer.objects.filter(id= logged_customer_id)) == 1:
            return Customer.objects.filter(id= logged_customer_id)
        else:
            return None
    else:
        return None
