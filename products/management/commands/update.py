import requests
import gzip
import json



from django.core.management.base import BaseCommand
from products.models import Product, Category


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

        # print(files_to_download)
        update_data = []
        for filename in files_to_download:
            req = requests.get(f'https://static.openfoodfacts.org/data/delta/{filename}', allow_redirects=True)
            with open(f'modified/{filename}', 'wb') as gz_file:
                gz_file.write(req.content)
    
            with gzip.open(f'modified/{filename}', 'rb') as gz_file:
                update_data.append(gz_file.read().decode())

        with open(f'modified/changelist/{filename}', 'w') as json_file:
            json_file.write(str(update_data))




