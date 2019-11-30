import unittest
from unittest import mock

from django.db.models import QuerySet

from store.management.commands.update_db import Command
from store.models import Categories, Products, Nutriments_for_100g

categories = ['Viandes']

fake_received_nutriments = {
    "fat_100g": "10,5",
    "saturated-fat_100g": "3.5",
    "sugars_100g": "2,5",
    "salt_100g": "1.8",
    "oder_nutriment1": "X,Y",
    "oder_nutriment2": "X,Y",
    "oder_nutriment3": "X,Y"
}

fake_received_data = {"products": [{"id": 1,
                                    "product_name": "name",
                                    "generic_name_fr": "name_generic",
                                    "brands": "brand_name",
                                    "nutrition_grade_fr": "a_to_e",
                                    "nova_groups": "1_to_4",
                                    "ingredients_text_fr": "ingredients",
                                    "url": "url_page",
                                    "image_url": "url_image",
                                    "nutriments": fake_received_nutriments,
                                    "categories": "oder_categorie",
                                    "countries_lc": "fr",
                                    "oder_param_x": "param_x",
                                    "oder_param_y": "param_y"
                                    }]
                      }

fake_result_filtered_nutriments = {"Matières grasses/lipides": "10,5",
                                   "Acide gras saturés": "3,5",
                                   "Sucres": "2,5",
                                   "Sel": "1,8"
                                   }

fake_result_filtered_data = [{"id": 1,
                              "product_name": "name",
                              "generic_name_fr": "name_generic",
                              "brands": "brand_name",
                              "nutrition_grade_fr": "a_to_e",
                              "nova_groups": "1_to_4",
                              "ingredients_text_fr": "ingredients",
                              "url": "url_page",
                              "image_url": "url_image",
                              "nutriments": fake_result_filtered_nutriments,
                              "categories": "oder_categorie",
                              }]


class command(unittest.TestCase):

    # This mock method will replace requests.get from "Command._search_api_data()"
    def mock_requests_get(self, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(fake_received_data, 200)

    @mock.patch('store.management.commands.update_db.requests.get', side_effect=mock_requests_get)
    def test_search_api_data(self, mock_get):
        result = Command._search_api_data(categories)
        self.assertEqual(result, fake_result_filtered_data)

    def test_filtered_api_data(self):
        result = Command._filtered_api_data(fake_received_data)
        self.assertEqual(result, fake_result_filtered_data)

    def test_filtered_nutriments(self):
        result = Command._filtered_nutriments(fake_received_nutriments)
        self.assertEqual(result, fake_result_filtered_nutriments)

    @mock.patch('store.management.commands.update_db.settings.CATEGORIES', categories)
    @mock.patch('store.management.commands.update_db.requests.get', side_effect=mock_requests_get)
    def test_update_db(self, mock_data):
        # Test if all data in database
        Command.update_db()
        self.assertEqual(len(Categories.objects.all()), 2)
        self.assertTrue(Products.objects.filter(pk=1).exists())
        product = Products.objects.get(pk=1)
        self.assertEqual(product.product_name, 'name')
        self.assertEqual(product.generic_name_fr, 'name_generic')
        self.assertEqual(product.brands, "brand_name")
        self.assertEqual(product.nutrition_grade_fr, "a_to_e")
        self.assertEqual(product.nova_groups, "1_to_4")
        self.assertEqual(product.ingredients_text_fr, "ingredients")
        self.assertEqual(product.url, "url_page")
        self.assertEqual(product.image_url, "url_image")
        self.assertTrue(Categories.objects.all().exists())
        self.assertTrue(Nutriments_for_100g.objects.all().exists())
        self.assertEqual(Nutriments_for_100g.objects.get(pk=1).name, 'Matières grasses/lipides')
        self.assertEqual(Nutriments_for_100g.objects.get(pk=1).quantity, '10,5')
        self.assertEqual(Nutriments_for_100g.objects.get(pk=2).name, 'Acide gras saturés')
        self.assertEqual(Nutriments_for_100g.objects.get(pk=2).quantity, '3,5')
        self.assertEqual(Nutriments_for_100g.objects.get(pk=3).name, 'Sucres')
        self.assertEqual(Nutriments_for_100g.objects.get(pk=3).quantity, '2,5')
        self.assertEqual(Nutriments_for_100g.objects.get(pk=4).name, 'Sel')
        self.assertEqual(Nutriments_for_100g.objects.get(pk=4).quantity, '1,8')


if __name__ == '__main__':
    unittest.main()
