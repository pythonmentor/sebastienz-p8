from django.db import models
from accounts.models import User


class Categories(models.Model):
    """ Categories table"""
    name = models.CharField(verbose_name='catégorie', max_length=50)

    def __str__(self):
        """ display name in shell"""
        return self.name


class Products(models.Model):
    """ Products table"""
    id = models.BigIntegerField(primary_key=True)
    categories = models.ManyToManyField(Categories, related_name="categories")
    substitutes = models.ManyToManyField('self', related_name='substitute', symmetrical=False,
                                         through="User_Favorites_Substitutes",
                                         through_fields=('prod_base', 'prod_substitute'))
    product_name = models.CharField(verbose_name='Nom du produit', max_length=150)
    generic_name_fr = models.CharField(verbose_name='Nom générique', max_length=300)
    brands = models.CharField(verbose_name='Marque', max_length=150)
    nutrition_grade_fr = models.CharField(verbose_name='Nutri-score', max_length=10)
    nova_groups = models.CharField(verbose_name='Groupe Nova', max_length=10)
    ingredients_text_fr = models.CharField(verbose_name="Liste d'Ingredients", max_length=2000)
    url = models.URLField(verbose_name='URL vers le produit', max_length=255)
    image_url = models.URLField(verbose_name="URL vers l'image du produit", max_length=255)

    def __str__(self):
        """ display product_name in shell"""
        return self.product_name

    class META:
        verbose_name = "Produits"


class Nutriments_for_100g(models.Model):
    """ Nutriments table"""
    id = models.BigAutoField(primary_key=True)
    product = models.ManyToManyField(Products, related_name="Produit")
    name = models.CharField(verbose_name='Non du nutriments', max_length=50)
    quantity = models.CharField(verbose_name="Quantité pour 100g", max_length=10)

    def __str__(self):
        return self.name

    class META:
        verbose_name = "Nutriments pour 100g"


class User_Favorites_Substitutes(models.Model):
    """ User saved substitutes table"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=True, related_name='user')
    prod_base = models.ForeignKey(Products, on_delete=True, related_name='prod_base')
    prod_substitute = models.ForeignKey(Products, on_delete=True, related_name='prod_substitute')

    class Meta:
        """ Add unique constrain of all three keys"""
        constraints = [
            models.UniqueConstraint(fields=['user', 'prod_base', 'prod_substitute'], name='unique_user_prod_sub')
        ]
