from django.test import TestCase
from django.urls import reverse

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