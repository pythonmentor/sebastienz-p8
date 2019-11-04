import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import DataError

from store.models import Categories, Products, Nutriments_for_100g, Substitutes


class Command:
    help = 'Read the data from Openfoodfacts and update the local database'

    @classmethod
    def _search_api_data(cls, categorie="Viandes"):
        off_url = 'https://fr.openfoodfacts.org/cgi/search.pl?'
        off_params = {
            "action": "process",
            "contries": "france",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "page_size": "1000",
            "json": "1",
            "tag_0": categorie,  # Search categorie
            # "search_terms": ""  # Search item
        }

        off_data = requests.get(off_url, off_params)
        off_products = off_data.json()
        filtered_off_data = cls._filtered_api_data(off_products)
        return filtered_off_data

    @classmethod
    def _filtered_api_data(cls, products_data):
        products_list = []
        product_items = {}
        needed_data = ["id",
                       "product_name",
                       "generic_name_fr",
                       "brands",
                       "nutrition_grade_fr",
                       "nova_groups",
                       "ingredients_text_fr",
                       "url",
                       "image_url",
                       "nutriments",
                       "categories"
                       ]

        for product in products_data["products"]:
            product_items = {}
            # Check if all key in products
            if all(key in product for key in needed_data):
                for key in needed_data:
                    # Check if all values in products and value not empty
                    if all(product.get(key) != '' for key in needed_data):
                        # if all(str(product[key])) and product[key] != ' ':
                        # if all(str([value for value in product[key]])):
                        if key == "nutriments":
                            product_items[key] = cls._filtered_nutriments(product[key])
                        else:
                            product_items[key] = product[key]
                        products_list.append(product_items)
        return products_list

    @classmethod
    def _filtered_nutriments(cls, nutriments):
        needed_nutriments_data = {
            "Matières grasses/lipides": "fat_100g",
            "Acide gras saturés": "saturated-fat_100g",
            "Sucres": "sugars_100g",
            "Sel": "salt_100g"
        }
        raw_nutriments = {}
        for key in nutriments.keys():
            if key in needed_nutriments_data.values():
                for fr_key, en_key in needed_nutriments_data.items():
                    raw_nutriments[fr_key] = nutriments.get(en_key)
        return raw_nutriments

    @classmethod
    def update_db(cls):
        for cat in settings.CATEGORIES:
            categorie_inst, created = Categories.objects.update_or_create(name=cat)
            products_list = cls._search_api_data(cat)

            for product in products_list:
                try:
                    db_product, created = Products.objects.update_or_create(**{key: value for (key, value)
                                                                               in product.items()
                                                                               if key in [fields.name for fields in
                                                                                          Products._meta.get_fields()]
                                                                               and key != "categories"})

                    for nutriment_name, quantity in product['nutriments'].items():
                        nutriment_inst, created = Nutriments_for_100g.objects.update_or_create(name=nutriment_name,
                                                                                               quantity=quantity)
                        nutriment_inst.product.add(db_product)

                    db_product.categories.add(categorie_inst)

                except DataError:
                    pass
