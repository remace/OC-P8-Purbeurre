from django.test import TestCase
from django.urls import reverse

from accounts.models import User
# Create your tests here.

class RegisterPageTextCase(TestCase):

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_new_user_registration_nominal_case(self):
        registered_user_old = User.objects.count()

        email="test@test.fr"
        password = "LePetitChevalDeManège123123!"
        last_name = "test last"
        first_name = "test first"

        response = self.client.post(reverse('register'),
                                                {'email':email,
                                                'password':password,
                                                'last_name':last_name,
                                                'first_name':first_name})
        
        registered_user_new = User.objects.count()
        
        self.assertEqual(registered_user_old + 1, registered_user_new)
        
    def test_new_user_registration_case_void_facultative_fields(self):
        registered_user_old = User.objects.count()

        email="test@test.fr"
        password = "LePetitChevalDeManège123123!"

        response = self.client.post(reverse('register'),
                                                {'email':email,
                                                'password':password,})
        
        registered_user_new = User.objects.count()
        
        self.assertEqual(registered_user_old + 1, registered_user_new)