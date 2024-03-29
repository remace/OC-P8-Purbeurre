import requests
import gzip
import json
from datetime import datetime

from django.core.management.base import BaseCommand
from products.models import Product, Category


def update_product(product: Product, product_dict: dict):
    product.name = product_dict.get('product_name')
    product.nutriscore = product_dict.get('nutriscore_grade', 'F').upper()
    product.energy_unit = product_dict.get('energy_unit')
    product.energy_100g = round(int(product_dict.get('nutriments').get('energy_100g')),9)
    product.carbohydrates_100g = round(int(product_dict.get('nutriments').get('carbohydrates_100g')),3)
    product.sugars_100g = round(int(product_dict.get('nutriments').get('sugars_100g')),3)
    product.fat_100g = round(int(product_dict.get('nutriments').get('fat_100g')),3)
    product.saturated_fat_100g = round(int(product_dict.get('nutriments').get('saturated_fat_100g')),3)
    product.fiber_100g = round(int(product_dict.get('nutriments').get('fiber_100g')),3)
    product.proteins_100g = round(int(product_dict.get('nutriments').get('proteins_100g')),3)
    product.salt_100g = round(int(product_dict.get('nutriments').get('salt_100g')),3)
    product.sodium_100g = round(int(product_dict.get('nutriments').get('sodium_100g')),3)
    product.updated_at = datetime.now()
    return product


class Command(BaseCommand):
    ''' populates the database with x products from y categories'''

    help = ("updates the database products with openfoodfacts changelist\n "
            "syntax: ./manage.py update")


    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        '''
        gets change list from openfoodfacts delta api
        https://static.openfoodfacts.org/data/delta/{filename}
        then compares last update timestamps.
        if a product in my base is outdated, update it.
        '''

        files_text = requests.get('https://static.openfoodfacts.org/data/delta/index.txt').text
        files_list = files_text.split('\n')
        files_to_download=files_list[0:7]

        for filename in files_to_download:

            # download update data archive
            req = requests.get(f'https://static.openfoodfacts.org/data/delta/{filename}', allow_redirects=True)
            with open(f'modified/{filename}', 'wb') as gz_file:
                gz_file.write(req.content)
        


        with open(f'modified/changelist/changelist.json', 'a') as json_file:
            for filename in files_to_download:
                # decode update data archive
                with gzip.open(f'modified/{filename}', 'rb') as gz_file:
                    update_data_list_strings = [data for data in gz_file.read().decode().split('\n') if data != ""]
                    update_data_list_dicts = []
                    for data in update_data_list_strings:
                        update_data_list_dicts.append(json.loads(data))
            json_file.write(str(update_data_list_dicts))

        count=0
        updated_count=0
        for product_dict in update_data_list_dicts:
            products = Product.objects\
                .filter(off_link=f' https://world.openfoodfacts.org/api/v0/product/{product_dict.get("id")}.json')\
                .filter(updated_at__gte=datetime.utcfromtimestamp(int(product_dict.get("last_modified_t"))/1000.0))\
                .all()
            count+=1
            if len(products)>=1:
                for product in products:
                    product = update_product(product, product_dict)
                updated_count+=len(products)

        print(f"{count} produits mis à jour chez open food facts\n {updated_count} mis à jour ici")
