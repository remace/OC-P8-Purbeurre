from django.test import TestCase
from django.urls import reverse
from .models import Category, Product
from accounts.models import User
# Create your tests here.

class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(reverse('index'))

class SearchPageTestCase(TestCase):
    def test_search_page(self):
        response = self.client.get(reverse('search')+'?search=Harry')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(reverse('search'))

class ProductPageTestCase(TestCase):
    def SetUp(self):
        user = User.objects.create_user(email='test@test.fr', password='coucou')
        user.save()
        category = Category(name='testing category')
        category.save()
        product = Product(
            name='produit favori de test',
            nutriscore='C',
            energy_unit = 'kJ',
            energy_100g = 3500,
            carbohydrates_100g = 30.7,
            sugars_100g = 14.0,
            fat_100g = 5.9,
            saturated_fat = 3.0,
            fiber_100g = 30.0,
            proteins_100g = 10.0,
            salt = 2.0,
            sodium = 0.15,
            off_link = 'lien_off',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = category,
            in_users_favourites=[user]
        )
        product.save()
        products = Product(
            name='produit non-favori de test',
            nutriscore='B',
            energy_unit = 'kJ',
            energy_100g = 3500,
            carbohydrates_100g = 30.7,
            sugars_100g = 14.0,
            fat_100g = 5.9,
            saturated_fat = 3.0,
            fiber_100g = 30.0,
            proteins_100g = 10.0,
            salt = 2.0,
            sodium = 0.15,
            off_link = 'lien_off',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = category,
            in_users_favourites=[user]
        )
        product2.save()
        product = Product.objects.get(name='produit favori de test')
        self.id = product.id

        def test_product_page(self):
            response = self.client.get(reverse('product')+f'?id={self.id}')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(reverse('product'))