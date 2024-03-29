''' a command that populates the database with data from openfoodfacts '''
import requests
from django.core.management.base import BaseCommand
from products.models import Product, Category

CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories.json'

def get_categories_from_openfoodfacts():
    ''' should get all the usable stuff from openfoodfacts '''
    response = requests.get(CATEGORIES_URL)
    return response.json()

def get_products_from_category(url, n_products):
    ''' get products from a given category url'''
    rep = []
    for page in range(1, int(n_products//24)+2):
        response = requests.get(url + "/" + str(page) + ".json")
        for product in response.json()['products']:
            rep.append(product)
    return rep

def create_product_or_None(prod : dict, category):
    """ given a dict, this function returns a product object if possible or none """
    try:
        if 'energy-kcal_100g' in prod['nutriments']:
            energy_unit = 'kcal'
            energy_100g = prod['nutriments'].get('energy-kcal_100g',-1)
        else:
            energy_unit = 'kJ'
            energy_100g = prod['nutriments'].get('energy-kj_100g',-1)

        if 'id' in prod:
            product = Product(
                name = prod['product_name'],
                nutriscore = prod.get('nutriscore_grade','F').upper(),
                energy_unit = energy_unit,
                energy_100g = round(energy_100g,9),
                carbohydrates_100g = round(prod['nutriments'].get('carbohydrates_100g',-1),3),
                sugars_100g = round(prod['nutriments'].get('sugars_100g',-1),3),
                fat_100g = round(prod['nutriments'].get('fat_100g',-1),3),
                saturated_fat_100g = round(prod['nutriments'].get('saturated_fat_100g',-1),3),
                fiber_100g = round(prod['nutriments'].get('fiber_100g',-1),3),
                proteins_100g = round(prod['nutriments'].get('proteins_100g',-1),3),
                salt_100g = round(prod['nutriments'].get('salt_100g',-1),3),
                sodium_100g = round(prod['nutriments'].get('sodium_100g',-1),3),
                off_link = f'https://fr.openfoodfacts.org/produit/{ prod["id"]}',
                off_thumb_link = prod['image_front_thumb_url'],
                off_img_link = prod['image_front_url'],
                category = category,
            )
            return product
        else:
            return None
    except KeyError as error:

        print(f'KeyError: {prod["product_name"]}\tclé:{error}'\
        f'\thttps://fr.openfoodfacts.org/api/v0/produit/{prod["id"]}.json'\
        f'\n=> produit ignoré'
        )
        return None

class Command(BaseCommand):
    ''' populates the database with x products from y categories'''

    help = ("populates the database with products and categories from Open Food Facts API\n "
            "syntax: ./manage.py populate products categories \n")


    def add_arguments(self, parser):
        parser.add_argument('n_products',
            nargs='+',
            type=int,
            help='number of products to import from each category'
            )
        parser.add_argument('n_categories',
            nargs='+',
            type=int,
            help='number of categories to import'
            )

    def handle(self, *args, **options):

        n_products = options['n_products'][0]
        n_categories = options['n_categories'][0]

        cats_json = get_categories_from_openfoodfacts()

        category = Category()
        for cat in range(n_categories):
            # ajouter catégorie
            category = Category(name=cats_json['tags'][cat]['name'])
            print(f'{cat+1}/{n_categories}\t{category.name}')
            category.save()
            products = get_products_from_category(
                    cats_json['tags'][cat]['url'],
                    n_products)[0:n_products]
            for prod in products:
                product = create_product_or_None(prod,category)
                if product is not None:
                    product.save()
                    