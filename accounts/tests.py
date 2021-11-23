""" tests for account module """
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
# Create your tests here.

class RegisterPageTestCase(TestCase):
    """ test on register page """

    def test_register_page(self):
        """ test base view """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(reverse('register'))

    def test_new_user_registration_nominal_case(self):
        """ test user registration in the nominal case"""
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
        """ test user registration with a void facultative field """
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
        """ test user registration when the email is alreadi taken """
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

        self.assertEqual(response.status_code,400)

    def test_user_registration_invalid_email(self):
        """ test user registration with an invalid email """
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

        self.assertEqual(response.status_code,400)


    def test_user_registration_short_password(self):
        """ test user registration with a password too short """
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
        self.assertEqual(response.status_code,400)

    def test_user_registration_unmatching_passwords(self):
        """ test user registration with different passwords """
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
        self.assertEqual(response.status_code,400)

class LoginTest(TestCase):
    """ class for testing Login view """
    def setUp(self):
        email="test@test.com"
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
        """ test template use and status code """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(reverse('login'))

    def test_user_login_nominal_case(self):
        """ test login in nominal case """
        email="test@test.com"
        password = "LePetitChevalDeManège123123!"
        response = self.client.post(reverse('login'),
                                                    {'email':email,
                                                    'password':password,})
        self.assertEqual(response.status_code,200)

    def test_user_login_unmatching_email(self):
        """ test user login with unmatching email """
        email="test222@test.com"
        password = "LePetitChevalDeManège123123!"
        response = self.client.post(reverse('login'),
                                                    {'email':email,
                                                    'password':password,})
        self.assertEqual(response.status_code, 400)

    def test_user_login_unmatching_password(self):
        """ test user login with unmatching password"""
        email="test@test.com"
        password = "LePetitChevalDeManège123123!222"
        response = self.client.post(reverse('login'),
                                                    {'email':email,
                                                    'password':password,})
        self.assertEqual(response.status_code, 400)

class LogoutTest(TestCase):
    """ test for logout view"""
    def test_logout_nominal_case(self):
        """ test logout nominal case"""
        email="test@test.com"
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
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code,200)

    def test_logout_user_not_logged_in(self):
        """ test logout when user is not logged in """
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 400)
