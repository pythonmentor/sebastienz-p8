from django.contrib.auth.decorators import login_required
from django.test import TestCase, Client
from django.urls import reverse

from .models import Categories, Products, Nutriments_for_100g, User_Favorites_Substitutes
from accounts.models import User


# Test store views
class IndexPageTestCase(TestCase):
    def test_display_index_page(self):
        # Call index page
        response = self.client.get('/')
        # Test if page is found
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
        response = self.client.get(reverse('store:substitutes', kwargs={'product_id': 0000}))
        self.assertEqual(response.status_code, 404)


class DetailPageTestCase(TestCase):
    def setUp(self):
        # Create a product
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
        # Create nutriments
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
        # Linked nutriments to the product
        nutriment1.product.add(self.product)
        nutriment2.product.add(self.product)

    def test_display_detail_page(self):
        # Call the detail page with create product and the nutriments for the detail
        # response = self.client.get('/store/1234/')
        response = self.client.get(reverse('store:details', kwargs={'product_id': self.product.id}))
        # Test status code when page is found
        self.assertEqual(response.status_code, 200)

    def test_detail_page_not_found(self):
        # Call the detail page with create product and the nutriments for the detail
        # response = self.client.get('/store/0000/')
        response = self.client.get(reverse('store:details', kwargs={'product_id': 0000}))
        # Test status code when page is not found
        self.assertEqual(response.status_code, 404)


class SaveSubstituteTestCase(TestCase):
    def setUp(self):
        # Create a user in database
        self.user = User.objects.create_user(email='fake_email@fake_email.com')
        self.user.set_password("fake_pass")
        self.user.save()
        # Logged_in the user
        self.client = Client()
        self.client.login(email='fake_email@fake_email.com', password="fake_pass")
        # Create a product in database
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
        # Create a substitute in database (A product with better nutrition grade)
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

    @login_required
    def test_save_redirection_page(self):
        # Call save substitute with created product and substitute
        response = self.client.get(reverse('store:save_substitute', kwargs={'product_id': self.product.id,
                                                                            'substitute_id': self.substitute.id}))
        # Test if page redirection
        self.assertEqual(response.status_code, 302)

    def test_if_favorit_is_saved(self):
        # Call save substitute with created product and substitute
        self.test_save_redirection_page()
        # Test if a favorite substitute has been created in database
        self.assertEqual(len(User_Favorites_Substitutes.objects.filter(prod_base=self.product.id, prod_substitute=self.
                                                                       substitute.id)), 1)


class DeleteSubstituteTestCase(TestCase):
    def setUp(self):
        # Create a user in database
        self.user = User.objects.create_user(email='fake_email@fake_email.com')
        self.user.set_password("fake_pass")
        self.user.save()
        # Logged_in the user
        self.client = Client()
        self.client.login(email='fake_email@fake_email.com', password="fake_pass")
        # Create a product in database
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
        # Create a substitute in database (A product with better nutrition grade)
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
        # Add product with substitute in favorites
        self.favorite = User_Favorites_Substitutes.objects.update_or_create(prod_base=self.product,
                                                                            prod_substitute=self.substitute,
                                                                            user=self.user)

    def test_delete_favorit(self):
        # Call delete favorite substitute
        self.client.get(reverse('store:delete_favorite', kwargs={'product_id': self.product.id,
                                                                 'substitute_id': self.substitute.id}))

        self.assertEqual(len(User_Favorites_Substitutes.objects.filter(prod_base=self.product.id, prod_substitute=self.
                                                                       substitute.id)), 0)
