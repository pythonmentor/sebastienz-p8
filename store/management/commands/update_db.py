import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import DataError

from store.models import Categories, Products, Nutriments_for_100g, Substitutes


class Command(BaseCommand):
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
            # Check if all key in products and all values in products are not empty
            if all(key in product for key in needed_data) and all(product.get(key) != '' for key in needed_data):
                for key in needed_data:
                    if key == "ingredients_text_fr":
                        product_items[key] = product[key].replace('_', '').lstrip()
                    elif key == "nutriments":
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
                    raw_nutriments[fr_key] = str(nutriments.get(en_key)).replace(".", ",")
        return raw_nutriments

    @classmethod
    def update_db(cls):
        for cat in settings.CATEGORIES:
            categorie_inst, created = Categories.objects.update_or_create(name=cat)
            products_list = cls._search_api_data(cat)
            for product in products_list:
                # if Products.objects.filter(id=product["id"]).exists() is False:
                try:
                    db_product, created = Products.objects.update_or_create(id=product['id'], defaults={key: value
                                                                            for (key, value) in product.items()
                                                                               if key in [fields.name for fields in
                                                                                          Products._meta.get_fields()]
                                                                               and key != "categories" and key != 'id'})

                    for nutriment_name, quantity in product['nutriments'].items():
                        nutriment_inst, created = Nutriments_for_100g.objects.update_or_create(name=nutriment_name,
                                                                                               quantity=quantity)
                        nutriment_inst.product.add(db_product)

                    for categorie in product['categories'].split(','):
                        categorie = "".join([string for string in categorie if not string.isdigit()])
                        if categorie[:3].lower() == "fr:":
                            categorie = categorie.lstrip('fr').strip(':').strip(' ').capitalize()
                        if (len(categorie) > 2) and (categorie[:3].lower() != 'en:'):
                            print(categorie)
                            cat_inst, created = Categories.objects.update_or_create(name=categorie)
                            print(db_product.product_name)
                            print(cat_inst)
                            db_product.categories.add(cat_inst)

                    db_product.categories.add(categorie_inst)

                except DataError:
                    pass

    def handle(self, *args, **options):
        """ Customer command that will be called """
        self.update_db()
