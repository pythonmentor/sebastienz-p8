from django.db import models

# Create your models here.

# class Customer(models.Model):
#     pseudo = models.CharField(verbose_name= "Pseudo", max_length = 50)
#     last_name = models.CharField(verbose_name= "Nom", max_length = 50, blank=True)
#     first_name = models.CharField(verbose_name="Prénom", max_length = 50, blank=True)
#     email = models.EmailField(verbose_name="Adresse mail", max_length= 100)
#     password = models.CharField(verbose_name="Mot de passe", max_length = 50)
#     def __str__(self):
#         return self.first_name+" "+self.last_name
#
#     class META:
#         verbose_name="Client"
