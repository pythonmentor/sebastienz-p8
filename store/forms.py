from django import forms


class SearchForm(forms.Form):
    search_product = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Rechercher',
        'id': 'search_form',
        'class': 'form-control col-8 offset-2 rounded-left', 'autofocus': 'true'
    }))

