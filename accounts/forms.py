from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django import forms
from django.forms.utils import ErrorList
from .models import Customer

class LoginForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'password']
        widgets = {
            'email' : EmailInput(attrs = {'class': 'form-control', 'placeholder': 'email'}),
            'password' : PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'mot de passe',}),
        }
    #email = forms.EmailField(label= 'Email', max_length= 100)
    #password = forms.CharField(label= "Mot de passe", widget= forms.PasswordInput, max_length= 50)

class RegisterForm(ModelForm):
    #last_name = forms.CharField(label= "Nom", max_length= 50)
    #first_name = forms.CharField(label= "Prénom", max_length= 50)
    #email = forms.EmailField(label= "Adresse mail", max_length= 100)
    class Meta:
        model = Customer
        fields = ['last_name', 'first_name', 'email', 'password']
        widgets = {
            'last_name' : TextInput(attrs = {'class': 'form-control', 'placeholder': 'nom'}),
            'first_name' : TextInput(attrs = {'class': 'form-control', 'placeholder': 'prénom'}),
            'email' : EmailInput(attrs = {'class': 'form-control', 'placeholder': 'email'}),
            'password' : PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'mot de passe',}),
        }
