from django.test import TestCase, Client
import requests
import unittest
from unittest import mock

from django.urls import reverse
from accounts.models import User
from products.models import Category, Product

from django.core.management import call_command
from products.management.commands.update import Command




def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'lien_off_1':
        return MockResponse({
                'name':'produit favori de test modifié',
                'nutriscore': 'B',
                'energy_unit': 'kJ',
                'energy_100g': 3500,
                'carbohydrates_100g': 30.7,
                'sugars_100g': 14.0,
                'fat_100g': 5.9,
                'saturated_fat_100g': 3.0,
                'fiber_100g': 30.0,
                'proteins_100g': 10.0,
                'salt_100g': 2.0,
                'sodium_100g': 0.15,
                'off_link': 'lien_off_1',
                'off_thumb_link': 'lien_thumb',
                'off_img_link': 'lien_image',
                }, 200)
    elif args[0] == 'lien_off_2':
        return MockResponse({
                'name':'produit non-favori de test',
                'nutriscore': 'B',
                'energy_unit': 'kJ',
                'energy_100g': 3500,
                'carbohydrates_100g': 30.7,
                'sugars_100g': 14.0,
                'fat_100g': 5.9,
                'saturated_fat_100g': 3.0,
                'fiber_100g': 30.0,
                'proteins_100g': 10.0,
                'salt_100g': 2.0,
                'sodium_100g': 0.15,
                'off_link': 'lien_off_2',
                'off_thumb_link': 'lien_thumb',
                'off_img_link': 'lien_image',
                }, 200)

    return MockResponse(None, 404)



class ProductMatcher:
    product: Product

    def __init__(self, product):
        self.product = product

    def __eq__(self, other):
        return self.product.name == other.name and \
            self.product.nutriscore == other.nutriscore and \
            self.product.energy_unit == other.energy_unit and \
            self.product.energy_100g == other.energy_100g and \
            self.product.carbohydrates_100g == other.carbohydrates_100g and \
            self.product.sugars_100g == other.sugars_100g and \
            self.product.fat_100g == other.fat_100g and \
            self.product.saturated_fat_100g == other.saturated_fat_100g and \
            self.product.fiber_100g == other.fiber_100g and \
            self.product.proteins_100g == other.proteins_100g and \
            self.product.salt_100g == other.salt_100g and \
            self.product.sodium_100g == other.sodium_100g and \
            self.product.off_link == other.off_link and \
            self.product.off_thumb_link == other.off_thumb_link and \
            self.product.off_img_link == other.off_img_link



class managementUpdateTestCase(TestCase):
    
    def setUp(self):

        # a normal user
        self.user = User.objects.create(email='coucou@coucou.fr', password='123456789')
        self.user.save()

        # a category
        self.category = Category(name='testing category')
        self.category.save()
        
        # a product that is in user's favourite list
        self.product = Product(
            name='produit favori de test',
            nutriscore='C',
            energy_unit = 'kJ',
            energy_100g = 3500,
            carbohydrates_100g = 30.7,
            sugars_100g = 14.0,
            fat_100g = 5.9,
            saturated_fat_100g = 3.0,
            fiber_100g = 30.0,
            proteins_100g = 10.0,
            salt_100g = 2.0,
            sodium_100g = 0.15,
            off_link = 'lien_off_1',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = self.category,
        )
        self.product.save()

        # a product that is not in user's favourite list
        self.product2 = Product(
            name='produit non-favori de test',
            nutriscore='B',
            energy_unit = 'kJ',
            energy_100g = 3500,
            carbohydrates_100g = 30.7,
            sugars_100g = 14.0,
            fat_100g = 5.9,
            saturated_fat_100g = 3.0,
            fiber_100g = 30.0,
            proteins_100g = 10.0,
            salt_100g = 2.0,
            sodium_100g = 0.15,
            off_link = 'lien_off_2',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = self.category,
        )
        self.product2.save()
        self.product = Product.objects.get(name='produit favori de test')
        self.product.in_users_favourites.add(self.user)
        self.product2 = Product.objects.get(name='produit non-favori de test')

    def tearDown(self):
        # clean all the database 
        Product.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

    @mock.patch('products.management.commands.update.requests.get', side_effect=mocked_requests_get)
    def test_only_the_modified_product_is_modified(self, *args, **kwargs):
        '''
            given two products, only the first one should be modified in database
        '''

        product_json = requests.get(self.product.off_link).json()
        product = Product(
            name=product_json.get('name'),
            nutriscore=product_json.get('nutriscore'),
            energy_unit=product_json.get('energy_unit'),
            energy_100g=product_json.get('energy_100g'),
            carbohydrates_100g=product_json.get('carbohydrates_100g'),
            sugars_100g=product_json.get('sugars_100g'),
            fat_100g=product_json.get('fat_100g'),
            saturated_fat_100g=product_json.get('saturated_fat-100g'),
            fiber_100g=product_json.get('fiber_100g'),
            proteins_100g=product_json.get('proteins_100g'),
            salt_100g=product_json.get('salt_100g'),
            sodium_100g=product_json.get('sodium_100g'),
            off_link=product_json.get('off_link'),
            off_thumb_link=product_json.get('off_thumb_link'),
            off_img_link=product_json.get('off_img_link'),
            category=self.category
        )


        product2_json = requests.get(self.product2.off_link).json()
        product2 = Product(
            name=product2_json.get('name'),
            nutriscore=product2_json.get('nutriscore'),
            energy_unit=product2_json.get('energy_unit'),
            energy_100g=product2_json.get('energy_100g'),
            carbohydrates_100g=product2_json.get('carbohydrates_100g'),
            sugars_100g=product2_json.get('sugars_100g'),
            fat_100g=product2_json.get('fat_100g'),
            saturated_fat_100g=product2_json.get('saturated_fat-100g'),
            fiber_100g=product2_json.get('fiber_100g'),
            proteins_100g=product2_json.get('proteins_100g'),
            salt_100g=product2_json.get('salt_100g'),
            sodium_100g=product2_json.get('sodium_100g'),
            off_link=product2_json.get('off_link'),
            off_thumb_link=product2_json.get('off_thumb_link'),
            off_img_link=product2_json.get('off_img_link'),
            category=self.category
        )

        self.assertEqual(ProductMatcher(self.product2), product2)
        self.assertNotEqual(ProductMatcher(self.product), product)
        
        self.call_command("update")

        self.assertEqual(ProductMatcher(self.product), product)
        self.assertEqual(ProductMatcher(self.product2), product2)        

    # @mock.patch('products.management.commands.update.requests.get', side_effect=mocked_requests_get)
    # def test_modified_favourite_product_stays_favourite(self):
        
    #     self.current_product = self.product

    #     # récupérer le mock de l'aliment modifié 
    #     product = requests.get(self.product.off_link)

    #     self.call_command("update")
                
    #     self.updated_product = self.product

    #     self.assertEqual(self.product.in_users_favourites, product.in_users_favourite)

