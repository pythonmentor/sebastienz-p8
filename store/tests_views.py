from django.contrib.auth.decorators import login_required
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import login, get_user

from store.forms import SearchForm
from .models import Categories, Products, Nutriments_for_100g, User_Favorites_Substitutes
from accounts.models import User


# Test view
class IndexPageTestCase(TestCase):
    def test_display_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ProductsPageTestCase(TestCase):
    def test_display_products_page(self):
        # Test if login page is loaded
        client = Client()
        response = client.get(reverse('store:products'))
        self.assertEqual(response.status_code, 200)


class SubstitutesPageTestCase(TestCase):
    def setUp(self):
        categorie = Categories.objects.create(name="Fake_categorie")
        self.product = Products(
            id=1234,
            product_name="Fake name1",
            generic_name_fr='Fake generic name1',
            brands='Fake brand',
            nutrition_grade_fr='e',
            nova_groups='4',
            ingredients_text_fr=" Fake text",
            url='https://fake-url1.com',
            image_url='https://fake-image-url1.com'
        )
        self.product.save()
        substitute = Products(
            id=4321,
            product_name="Fake name2",
            generic_name_fr='Fake generic name2',
            brands='Fake brand',
            nutrition_grade_fr='d',
            nova_groups='4',
            ingredients_text_fr=" Fake text",
            url='https://fake-url2.com',
            image_url='https://fake-image-url2.com'
        )
        substitute.save()
        self.product.categories.add(categorie)
        substitute.categories.add(categorie)

    def test_display_substitutes_page(self):
        # response = self.client.get('/store/1234/substitutes/')
        response = self.client.get(reverse('store:substitutes', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)

    def test_substitutes_page_not_found(self):
        # response = self.client.get('/store/1234/substitutes/')
        response = self.client.get(reverse('store:substitutes', kwargs={'product_id': 1234}))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):
    def setUp(self):
        self.product = Products(
            id=1234,
            product_name='Fake name',
            generic_name_fr='Fake generic name',
            brands='Fake brand',
            nutrition_grade_fr='b',
            nova_groups='4',
            ingredients_text_fr=" Fake text",
            url='https://fake-url.com',
            image_url='https://fake-image-url.com'
        )
        self.product.save()
        nutriment1 = Nutriments_for_100g(
            id=1,
            name='Fake_nutriment1',
            quantity='18,2'
        )
        nutriment1.save()
        nutriment2 = Nutriments_for_100g(
            id=2,
            name='Fake_nutriment2',
            quantity='15,7'
        )
        nutriment2.save()

        nutriment1.product.add(self.product)
        nutriment2.product.add(self.product)

    def test_display_detail_page(self):
        # response = self.client.get('/store/1234/')
        response = self.client.get(reverse('store:details', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_not_found(self):
        # response = self.client.get('/store/0000/')
        response = self.client.get(reverse('store:details', kwargs={'product_id': 0000}))
        self.assertEqual(response.status_code, 404)


class SaveSubstitutePageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='fake_email@fake_email.com', password="fake_pass")
        self.product = Products(
            id=1234,
            product_name="Fake name1",
            generic_name_fr='Fake generic name1',
            brands='Fake brand',
            nutrition_grade_fr='e',
            nova_groups='4',
            ingredients_text_fr=" Fake text",
            url='https://fake-url1.com',
            image_url='https://fake-image-url1.com'
        )
        self.product.save()
        self.substitute = Products(
            id=4321,
            product_name="Fake name2",
            generic_name_fr='Fake generic name2',
            brands='Fake brand',
            nutrition_grade_fr='d',
            nova_groups='4',
            ingredients_text_fr=" Fake text",
            url='https://fake-url2.com',
            image_url='https://fake-image-url2.com'
        )
        self.substitute.save()

    @login_required(login_url='accounts:login')
    def test_Save_redirection_page(self):
        response = self.client.get(reverse('store:save_substitute', kwargs={'product_id': self.product.id,
                                                                            'substitute_id': self.substitute.id}))
        # Test if page redirection
        self.assertEqual(response.status_code, 302)


