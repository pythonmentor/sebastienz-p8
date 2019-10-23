from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate, get_user

from accounts.forms import RegisterForm, LoginForm
from .models import User
from .views import user_login, user_register, user_logout, user_account, user_products


# Create your tests here.

class LoginPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='Sebastien@fakemail.com')
        self.user.set_password('fake_password')
        self.user.save()
        self.good_user_data = {'email': 'Sebastien@fakemail.com',
                               'password': 'fake_password'}
        self.bad_user_data = {'email': 'Sebastien',
                              'password': 'fake'}

    def test_display_login_page(self):
        # Test if login page is loaded
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_form_is_valid(self):
        """Test if login form with good user data is valid"""
        loginForm = LoginForm(self.good_user_data)
        self.assertTrue(loginForm.is_valid())

    def test_form_is_not_valid(self):
        """Test if login form with bad user data is invalide"""
        loginForm = LoginForm(self.bad_user_data)
        self.assertFalse(loginForm.is_valid())

    def test_login_page_with_good_user_data(self):
        """ If user data are good, then is the user is authenticate and redirect to index page """
        client = Client()
        response = client.post(reverse('accounts:login'), self.good_user_data)
        # Test if user is authenticate
        user = get_user(client)
        self.assertTrue(user.is_authenticated)
        # Test if page redirection
        self.assertEqual(response.status_code, 302)

    def test_login_page_with_bad_user_data(self):
        """ If user data are bad, user is not authenticate and refresh the login page """
        client = Client()
        response = client.post(reverse('accounts:login'), self.bad_user_data)
        user = get_user(client)
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 200)


class RegisterPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='Sebastien@fakemail.com', password='fake_password')
        self.user.save()
        # Neu user data, not exist in database
        self.good_user_data = {'email': 'Sebastien@anotherfakemail.com',
                               'password1': 'another_fake_password',
                               'password2': 'another_fake_password'}
        # User already exists in database
        self.bad_user_data = {'email': 'Sebastien@fakemail.com',
                              'password1': 'fake_password',
                              'password2': 'fake_password'}

    def test_display_register_page(self):
        # Test if register page is loaded
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_form_is_valid(self):
        # Test if register form with bad user data is valide
        registerForm = RegisterForm(self.good_user_data)
        self.assertTrue(registerForm.is_valid())

    def test_form_is_not_valid(self):
        # Test if register form with bad user data is invalide
        registerForm = RegisterForm(self.bad_user_data)
        self.assertFalse(registerForm.is_valid())

    def test_register_page_registration_with_good_user_data(self):
        """ If user entries are god, then is the user is authenticate and redirect to index page """
        client = Client()
        response = client.post(reverse('accounts:register'), self.good_user_data)
        # Test if user is authenticate
        user = get_user(client)
        self.assertTrue(user.is_authenticated)
        # Test if user is not saved in database
        # One user is already saved in database in setUp also yet must be two user saved
        user_in_database = len(User.objects.all())
        self.assertEqual(user_in_database, 2)
        # Test if page redirection
        self.assertEqual(response.status_code, 302)

    def test_register_page_registration_with_bad_user_data(self):
        """ If user entries are bad, user is not authenticate and refresh the login page """
        client = Client()
        response = client.post(reverse('accounts:register'), self.bad_user_data)
        # Test if user is not authenticate
        user = get_user(client)
        self.assertFalse(user.is_authenticated)
        # Test if user is not saved in database
        # One user is already saved in database in setUp also yet must be only one user saved
        user_in_database = len(User.objects.all())
        self.assertEqual(user_in_database, 1)
        # Test if reload the page
        self.assertEqual(response.status_code, 200)


class AccountPageTestCase(TestCase):
    pass
    # def setUp(self):
    #   user = CustomUser.objects.create(username='Sebastien@fakemail.com', password='fake_password')
    #   user.save()

    # def test_display_account_page(self):
    #     response = self.client.get(reverse('accounts:myaccount'))
    #     self.assertEqual(response.status_code, 200)
