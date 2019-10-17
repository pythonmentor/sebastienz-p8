from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Pseudo",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "pseudo"}))
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'mot de passe'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Pseudo",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "pseudo"}))
    last_name = forms.CharField(label="Nom",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nom'}))
    first_name = forms.CharField(label="Prénom",
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'prénom'}))
    email = forms.EmailField(label="Adresse électronique :", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password1 = forms.CharField(label="Mot de passe",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'mot de passe'}))
    password2 = forms.CharField(label="Confirmation mot de passe",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'mot de passe'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'last_name', 'first_name', 'email', 'password1')


class AccountForm(ModelForm):
    username = forms.CharField(label="Pseudo",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "pseudo"}))
    last_name = forms.CharField(label="Nom",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nom'}))
    first_name = forms.CharField(label="Prénom",
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'prénom'}))
    email = forms.EmailField(label="Adresse électronique :", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))

    class Meta(ModelForm):
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')
