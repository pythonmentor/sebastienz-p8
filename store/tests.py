# from django.test import TestCase
import requests
import unittest
from unittest import mock
from store.management.commands.update_db import Command


class command(unittest.TestCase):
    def setUp(self):
        self.categories = ['Viandes']
        self.url = 'https://fr.openfoodfacts.org/cgi/search.pl?action=process&contries=france&tagtype_0=categories' \
                   '&tag_contains_0=contains&page_size=1000&json=1&tag_0=Viandes'

        self.off_url = 'https://fr.openfoodfacts.org/cgi/search.pl?'
        self.off_params = {
            "action": "process",
            "contries": "france",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "page_size": "1000",
            "json": "1",
            "tag_0": self.categories,  # Search categorie
            # "search_terms": ""  # Search item
        }

        self.fake_received_nutriments = {
            "fat_100g": "quatity_fat_for_100g",
            "saturated-fat_100g": "quantity_saturated-fat_100g",
            "sugars_100g": "quantity_sugars_100g",
            "salt_100g": "quantity_salt_100g",
            "oder_nutriment1": "oder_data1",
            "oder_nutriment2": "oder_data2",
            "oder_nutriment3": "oder_data3"
        }

        self.fake_received_data = {"products": [{"id": "product_id",
                                                 "product_name": "name",
                                                 "generic_name_fr": "name_generic",
                                                 "brands": "brand_name",
                                                 "nutrition_grade_fr": "a_to_e",
                                                 "nova_groups": "1_to_4",
                                                 "ingredients_text_fr": "ingredients",
                                                 "url": "url_page",
                                                 "image_url": "url_image",
                                                 "nutriments": self.fake_received_nutriments,
                                                 "categories": "name_categories",
                                                 "oder_param_x": "param_x",
                                                 "oder_param_y": "param_y"
                                                 }]
                                   }

        self.fake_result_filtered_nutriments = {"Matières grasses/lipides": "quatity_fat_for_100g",
                                                "Acide gras saturés": "quantity_saturated-fat_100g",
                                                "Sucres": "quantity_sugars_100g",
                                                "Sel": "quantity_salt_100g"
                                                }

        self.fake_result_filtered_data = [{"id": "product_id",
                                           "product_name": "name",
                                           "generic_name_fr": "name_generic",
                                           "brands": "brand_name",
                                           "nutrition_grade_fr": "a_to_e",
                                           "nova_groups": "1_to_4",
                                           "ingredients_text_fr": "ingredients",
                                           "url": "url_page",
                                           "image_url": "url_image",
                                           "nutriments": self.fake_result_filtered_nutriments,
                                           "categories": "name_categories",
                                           }]

    # This mock method will replace requests.get from "Command._search_api_data()"
    def mock_requests_get(self, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if args[0] == self.off_url and kwargs == self.off_params:
            return MockResponse(self.fake_received_data, 200)
        else:
            return MockResponse(None, 404)

    @mock.patch('store.management.commands.update_db.requests.get', side_effect=mock_requests_get)
    def test_search_api_data(self):
        result = Command._search_api_data(self.categories)
        self.assertEqual(result, self.fake_result_filtered_data)

    def test_filtered_api_data(self):
        result = Command._filtered_api_data(self.fake_received_data)
        self.assertEqual(result, self.fake_result_filtered_data)

    def test_filtered_nutriments(self):
        result = Command._filtered_nutriments(self.fake_received_nutriments)
        self.assertEqual(result, self.fake_result_filtered_nutriments)

    def test_update_db(self):
        cat = "Viandes"



if __name__ == '__main__':
    unittest.main()
