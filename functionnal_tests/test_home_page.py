from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.urls import reverse

class TestFonctionnel(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def test_functionnal_search_page(self):
            """ search form should redirect to search URL with search parameter in url"""  
            self.browser.get(self.live_server_url)
            search_field = self.browser.find_element_by_id("main-search")
            search_field.clear()
            request = "produit"
            search_field.send_keys(request)
            submit = self.browser.find_element_by_id("main-search-sumbit")
            submit.click()
            self.assertEqual(self.browser.current_url,self.live_server_url+reverse('search')+"?search="+request)