from django.test import TestCase
from django.urls import reverse

from accounts.forms import RegisterForm
from .models import CustomUser


# Create your tests here.

class LoginPageTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(email='Sebastien@fakemail.com', password='fake_password')
        user.save()

    def test_display_login_page(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_post_login_page(self):
        context = {'email': 'Sebastien@fakemail.com', 'password': 'fake_password'}
        response = self.client.post(reverse('accounts:login'), context)
        self.assertEqual(response.status_code, 200)


class RegisterPageTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(email='Sebastien@fakemail.com', password='fake_password')
        user.save()

    def test_display_register_page(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_form_is_valid(self):
        registerForm = RegisterForm({'email': 'email@fakemail.com',
                                     'password1': 'fake_password',
                                     'password2': 'fake_password'})
        self.assertTrue(registerForm.is_valid())

    def test_form_is_not_valid(self):
        registerForm = RegisterForm({'email': 'email@fakemail.com',
                                     'password1': 'fake_password',
                                     'password2': 'false_password'})
        self.assertFalse(registerForm.is_valid())
