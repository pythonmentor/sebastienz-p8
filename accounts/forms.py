from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User


class LoginForm(forms.Form):
    """Define the login form"""
    email = forms.EmailField(label="Adresse électronique :", required=True,
                                widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'mot de passe'}))

    class Meta:
        model = User
        fields = ['email', 'password']


class RegisterForm(UserCreationForm):
    """Define the register form"""
    username = forms.CharField(label="Nom d'utilisateur (optionnel)", required=False,
                                widget=forms.TextInput(attrs={'id': 'username', 'class': 'form-control',
                                                               'placeholder': "nom d'utilisateur"}))
    email = forms.EmailField(label="Adresse électronique", required=True,
                                error_messages={'unique': "Cette adresse mail à déjà été enregistré !"},
                                widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control',
                                                               'placeholder': "email"}))
    last_name = forms.CharField(label="Nom (optionnel)", required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nom'}))
    first_name = forms.CharField(label="Prénom (optionnel)", required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'prénom'}))
    password1 = forms.CharField(label="Mot de passe",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'mot de passe'}))
    password2 = forms.CharField(label="Confirmation du mot de passe",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'mot de passe'}))

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'password1', 'password2']


class AccountForm(ModelForm):
    """Define the accounts form"""
    username = forms.CharField(label="Nom d'utilisateur", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true',
                                                             'placeholder': "pseudo"}))
    last_name = forms.CharField(label="Nom", required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true',
                                                              'placeholder': 'nom'}))
    first_name = forms.CharField(label="Prénom", required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true',
                                                               'placeholder': 'prénom'}))
    email = forms.EmailField(label="Adresse électronique :", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'true',
                                                            'placeholder': 'email'}))

    class Meta(ModelForm):
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')
