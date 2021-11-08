from django.test import TestCase
from django.urls import reverse

from accounts.models import User
# Create your tests here.

class RegisterPageTestCase(TestCase):

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(reverse('register'))

    def test_new_user_registration_nominal_case(self):
        registered_user_old = User.objects.count()

        email="test2@test.fr"
        password = "LePetitChevalDeManège123123!"
        last_name = "test last"
        first_name = "test first"

        response = self.client.post(reverse('register'),
                                                {'email':email,
                                                'password':password,
                                                'password2':password,
                                                'last_name':last_name,
                                                'first_name':first_name})
        registered_user_new = User.objects.count()
        self.assertEqual(registered_user_old + 1, registered_user_new)
        self.assertEqual(response.status_code,302)
        
    def test_new_user_registration_case_void_facultative_fields(self):
        registered_user_old = User.objects.count()

        email="test@test.fr"
        password = "LePetitChevalDeManège123123!"

        response = self.client.post(reverse('register'),
                                                {'email':email,
                                                'password':password,
                                                'password2':password})
        
        registered_user_new = User.objects.count()
        self.assertEqual(registered_user_old + 1, registered_user_new)
        self.assertEqual(response.status_code,302)

    def test_user_registration_already_taken_email(self):
        email="test@test.fr"
        password = "LePetitChevalDeManège123123!"
        last_name = "test last"
        first_name = "test first"
        self.client.post(reverse('register'),
                                    {'email':email,
                                    'password':password,
                                    'password2':password,
                                    'last_name':last_name,
                                    'first_name':first_name})
        
        response = self.client.post(reverse('register'),
                                                {'email':email,
                                                'password':password,
                                                'password2':password,
                                                'last_name':last_name,
                                                'first_name':first_name})

        self.assertEquals(response.status_code,400)

    def test_user_registration_invalid_email(self):
        email="test_email_invalide"
        password = "LePetitChevalDeManège123123!"
        last_name = "test last"
        first_name = "test first"        
        response = self.client.post(reverse('register'),
                                                {'email':email,
                                                'password':password,
                                                'password2':password,
                                                'last_name':last_name,
                                                'first_name':first_name})

        self.assertEquals(response.status_code,400)

    
    def test_user_registration_short_password(self):
        email="test-password@trop.court"
        password = "pass"
        last_name = "test last"
        first_name = "test first"        
        response = self.client.post(reverse('register'),
                                                {'email':email,
                                                'password':password,
                                                'password2':password,
                                                'last_name':last_name,
                                                'first_name':first_name})

    def test_user_registration_unmatching_passwords(self):
        email="test-password@diff.erents"
        password = "LePetitChevalDeManège123123!"
        password2 = "LePetitChevalDeManège123123!0"
        last_name = "test last"
        first_name = "test first"        
        response = self.client.post(reverse('register'),
                                                {'email':email,
                                                'password':password,
                                                'password2':password2,
                                                'last_name':last_name,
                                                'first_name':first_name})


class LoginTest(TestCase):

    def setUp(self):
        email="test-password@diff.erents"
        password = "LePetitChevalDeManège123123!"
        password2 = "LePetitChevalDeManège123123!"
        last_name = "test last"
        first_name = "test first"        
        self.client.post(reverse('register'),
                                    {'email':email,
                                    'password':password,
                                    'password2':password2,
                                    'last_name':last_name,
                                    'first_name':first_name})
    
    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(reverse('login'))

    def test_user_login_nominal_case(self):
        email="test-password@diff.erents"
        password = "LePetitChevalDeManège123123!"
        response = self.client.post(reverse('register'),
                                                    {'email':email,
                                                    'password':password,})
        self.assertEqual(response.status_code,200)

    def test_user_login_unmatching_email(self):
        pass

    def test_user_login_unmatching_password(self):
        pass