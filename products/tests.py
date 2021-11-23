from django.test import TestCase, Client

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
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='coucou@coucou.fr', password='123456789')
        self.user.save()

        self.category = Category(name='testing category')
        self.category.save()
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
            off_link = 'lien_off',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = self.category,
        )
        self.product.save()
        self.product.in_users_favourites.add(self.user)
        self.product.save()

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
            off_link = 'lien_off',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = self.category,
        )
        self.product2.save()
        self.product = Product.objects.get(name='produit non-favori de test')
        self.product2 = Product.objects.get(name='produit favori de test')

    def test_product_page(self):
        response = self.client.get(reverse('product')+f'?id={self.product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(reverse('product'))

    def test_product_page_nutriment_data(self):
        response = self.client.get(reverse('product')+f'?id={self.product.id}')
        self.assertEqual(response.context['product']['name'],self.product.name)
        self.assertEqual(response.context['product']['nutriscore'],self.product.nutriscore)
        self.assertEqual(response.context['product']['energy_unit'],self.product.energy_unit)
        self.assertEqual(response.context['product']['energy_100g'],self.product.energy_100g)
        self.assertEqual(response.context['product']['carbohydrates_100g'],self.product.carbohydrates_100g)
        self.assertEqual(response.context['product']['sugars_100g'],self.product.sugars_100g)
        self.assertEqual(response.context['product']['fat_100g'],self.product.fat_100g)
        self.assertEqual(response.context['product']['saturated_fat_100g'],self.product.saturated_fat_100g)
        self.assertEqual(response.context['product']['fiber_100g'],self.product.fiber_100g)
        self.assertEqual(response.context['product']['proteins_100g'],self.product.proteins_100g)
        self.assertEqual(response.context['product']['salt_100g'],self.product.salt_100g)
        self.assertEqual(response.context['product']['sodium_100g'],self.product.sodium_100g)
        self.assertEqual(response.context['product']['off_link'],self.product.off_link)
        self.assertEqual(response.context['product']['off_thumb_link'],self.product.off_thumb_link)
        self.assertEqual(response.context['product']['off_img_link'],self.product.off_img_link)
        self.assertEqual(response.context['product']['category'],self.product.category.name)


    def test_product_user_not_logged_in(self):
        response = self.client.get(reverse('product')+f'?id={self.product.id}')
        self.assertEqual(response.context['favourite_toggle_inactive'] , True)

    def test_product_nominal_case_in_favourite(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('product')+f'?id={self.product2.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'].get('is_favourite','favori'), True, msg=f"message: {response.context['product']}")

    def test_product_nominal_case_not_in_favourite(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('product')+f'?id={self.product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'].get('is_favourite','pas favori'), False, msg=f"message: {response.context['product']}")

    def test_product_non_existing(self):
        response = self.client.get(reverse('product')+'?id=50')
        self.assertEqual(response.status_code, 404)

class ListFavouritesTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='coucou@coucou.fr', password='123456789')
        self.user.save()
        self.user2 = User.objects.create(email='coucou2@coucou.fr', password='123456789')
        self.user2.save()
        self.category = Category(name='testing category')
        self.category.save()
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
            off_link = 'lien_off',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = self.category,
        )
        self.product.save()
        self.product.in_users_favourites.add(self.user)
        self.product.save()
        pass

    def test_list_favourites_page_nominal_case(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('list-favourites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(reverse('search'))
        

    def test_list_favourite_user_not_logged_in(self):
        response = self.client.get(reverse('list-favourites'))
        self.assertEqual(response.status_code, 302)

    def test_list_favourites_zero_favourite(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('list-favourites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(reverse('search'))


class ToggleFavouriteTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='coucou@coucou.fr', password='123456789')
        self.user.save()
        self.category = Category(name='testing category')
        self.category.save()
        self.product = Product(
            name='produit de test',
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
            off_link = 'lien_off',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = self.category,
        )
        self.product.save()

    def test_toggle_favourite_nominal_case(self):
        self.client.force_login(self.user)
        payload={}
        payload['product_id'] = self.product.id
        db_count_before = Product.objects.filter(in_users_favourites__id=self.user.id).count()
        response = self.client.post(reverse('toggle-favourite'), payload)
        db_count_after_add = Product.objects.filter(in_users_favourites__id=self.user.id).count()
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(reverse('product'))
        self.assertEqual(db_count_before+1,db_count_after_add)
        response = self.client.post(reverse('toggle-favourite'), payload)
        db_count_after_remove = Product.objects.filter(in_users_favourites__id=self.user.id).count()
        self.assertEqual(db_count_before,db_count_after_remove)

    def test_toggle_favourite_user_not_logged_in(self):
        payload={}
        payload['product_id'] = self.product.id
        db_count_before = Product.objects.filter(in_users_favourites__id=self.user.id).count()
        response = self.client.post(reverse('toggle-favourite'), payload)
        db_count_after_add = Product.objects.filter(in_users_favourites__id=self.user.id).count()
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(reverse('login'))

class FindAlternativesTestCase(TestCase):
    
    def setUp(self):
        self.category = Category(name='testing category')
        self.category.save()
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
            off_link = 'lien_off',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = self.category,
        )
        self.product.save()

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
            off_link = 'lien_off',
            off_thumb_link = 'lien_thumb',
            off_img_link= 'lien_image',
            category = self.category,
        )
        self.product2.save()

    def test_find_alternatives_nominal_case(self):
        response = self.client.get(reverse('find-alternatives')+f"?product_id={self.product.id}")
        products = response.context['results'] or null
        has_worse = False
        if products:
            for p in products:
                if p.nutriscore > self.product.nutriscore:
                    has_worse = True
        self.assertEqual(has_worse, False)

    def test_find_alternatives_no_better_nutriscore(self):
        response = self.client.get(reverse('find-alternatives')+f"?product_id={self.product2.id}")
        products = response.context['results'] or null
        has_worse = False
        if products:
            for p in products:
                if p.nutriscore > self.product.nutriscore:
                    has_worse = True
        self.assertEqual(has_worse, False)