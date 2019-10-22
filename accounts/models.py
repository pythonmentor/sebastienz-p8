import re

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    nickname = models.CharField(verbose_name="Pseudo", blank=True, unique=False, max_length=50)
    last_name = models.CharField(verbose_name="Nom", max_length=150, blank=True)
    first_name = models.CharField(verbose_name="Prénom", max_length=150, blank=True)
    email = models.EmailField(verbose_name="Adresse mail", blank=False, unique=True, max_length=150)
    password = models.CharField(verbose_name="Mot de passe", max_length=150)

    def __str__(self):
        return self.email

    def formated_username(self):
        regex = r"\w+"
        return re.findall(regex, self.username)[0]

    class META:
        verbose_name = "Client"
