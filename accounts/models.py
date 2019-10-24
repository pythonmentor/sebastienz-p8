import re

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("L'adresse email est requise")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le super utilisateur doit avoir 'is_staff=True'.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le super utilisateur doit avoir 'is_superuser=True'.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(verbose_name="Nom d'utilisateur", blank=True, unique=False, max_length=50)
    last_name = models.CharField(verbose_name="Nom", max_length=150, blank=True)
    first_name = models.CharField(verbose_name="Prénom", max_length=150, blank=True)
    email = models.EmailField(verbose_name="Adresse mail", blank=False, unique=True, max_length=150)
    password = models.CharField(verbose_name="Mot de passe", max_length=150)

    def __str__(self):
        return str(self.id) + ": " + self.email

    def formated_email(self):
        regex = r"\w+"
        return re.findall(regex, self.email)[0]

    class META:
        verbose_name = "Client"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
