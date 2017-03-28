import unittest
from django.test import Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
# Create your tests here.


class DataTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_missing_data(self):

        # missing first_name
        response = self.client.post(reverse('maro_auth:signup'), {'last_name': 'smith', 'email': 'a123456@dac.unicamp.br'})

        # Check that the response is not 302, redirected
        self.assertNotEqual(response.status_code, 302)

        # missing last_name
        response = self.client.post(reverse('maro_auth:signup'), {'first_name': 'john', 'email': 'a123456@dac.unicamp.br'})

        # Check that the response is not 302, redirected
        self.assertNotEqual(response.status_code, 302)

        # missing email
        response = self.client.post(reverse('maro_auth:signup'), {'first_name': 'john', 'first_name': 'john'})

        # Check that the response is not 302, redirected
        self.assertNotEqual(response.status_code, 302)


class SignupTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_signup_and_confirm_email(self):

        # sign someone up
        response = self.client.post(reverse('maro_auth:signup'), {'first_name': 'john', 'last_name': 'smith', 'email': 'a123456@dac.unicamp.br'})

        # Check that the response is 302, redirected
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(first_name='john')
        self.assertFalse(user.emailmanager.is_active)
        self.assertIsNotNone(user.emailmanager.key)
        self.assertEqual(user.emailmanager.active_email, 'a123456@dac.unicamp.br')

        # verify their email
        response = self.client.post(reverse('maro_auth:password_set', kwargs={'key': user.emailmanager.key}), {'new_password1': 'a_password1', 'new_password2': 'a_password1'})

        self.assertEqual(response.status_code, 302)

        user = User.objects.get(email='a123456@dac.unicamp.br')
        self.assertTrue(user.emailmanager.is_active)


class ChangeEmailTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_change_email(self):

        # sign someone up
        response = self.client.post(reverse('maro_auth:signup'), {'first_name': 'john1', 'last_name': 'smith1', 'email': 'b123456@dac.unicamp.br'})

        user = User.objects.get(first_name='john1')

        # verify their email
        self.client.post(reverse('maro_auth:password_set', kwargs={'key': user.emailmanager.key}), {'new_password1': 'a_password1', 'new_password2': 'a_password1'})

        key = user.emailmanager.change_email('newemail@gm2.com')

        self.assertEqual(key, user.emailmanager.key)
        self.assertNotEqual('newemail@gm2.com', user.emailmanager.active_email)
        self.assertEqual('newemail@gm2.com', user.emailmanager.other_email)
        self.assertEqual('b123456@dac.unicamp.br', user.email)
        self.assertEqual('b123456@dac.unicamp.br', user.username)

        # verify email change
        response = self.client.post(reverse('maro_auth:change_email', kwargs={'key': key}))

        self.assertEqual(response.status_code, 302)

        user = User.objects.get(first_name='john1')

        self.assertEqual(key, user.emailmanager.key)
        self.assertEqual('newemail@gm2.com', user.emailmanager.other_email)
        self.assertEqual('newemail@gm2.com', user.username)
        self.assertEqual('newemail@gm2.com', user.emailmanager.active_email)
        self.assertEqual('newemail@gm2.com', user.email)
