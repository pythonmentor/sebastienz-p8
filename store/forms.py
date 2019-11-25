from django import forms


class SearchForm(forms.Form):
    search_product = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Produit',
        'id': 'search_form',
        'class': 'rounded col-md-6 col-md-offset-3','autofocus':'true'
    }))

