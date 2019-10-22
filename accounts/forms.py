from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.EmailField(label="Adresse électronique :", required=True,
                                widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'mot de passe'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class RegisterForm(UserCreationForm):
    username = forms.EmailField(label="Adresse électronique", required=True,
                                error_messages={'unique': "Cette adresse mail à déjà été enregistré !"},
                                widget=forms.EmailInput(attrs={'id': 'username', 'class': 'form-control',
                                                               'placeholder': "email"}))
    nickname = forms.CharField(label="Pseudo (optionnel)", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "pseudo"}))
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
        model = CustomUser
        fields = ['nickname', 'last_name', 'first_name', 'username', 'password1', 'password2']


class AccountForm(ModelForm):
    nickname = forms.CharField(label="Pseudo", required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true',
                                                             'placeholder': "pseudo"}))
    last_name = forms.CharField(label="Nom",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true',
                                                              'placeholder': 'nom'}))
    first_name = forms.CharField(label="Prénom",
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true',
                                                               'placeholder': 'prénom'}))
    username = forms.EmailField(label="Adresse électronique :", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'disabled': 'true',
                                                            'placeholder': 'email'}))

    class Meta(ModelForm):
        model = CustomUser
        fields = ('nickname', 'last_name', 'first_name', 'username')
