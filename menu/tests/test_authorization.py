from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.test import Client

User = get_user_model()


class AuthorizationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@test.pl', 'test')
        self.client.login(username='test', password='test')
        self.token, created = Token.objects.get_or_create(user=self.user)

    def test__menu_add_authorization(self):
        data_to_add = {
            "name": "Kuchnia Francuzka",
            "description": "Kuchnia Francuzka",
            "dishes": [
                2, 5, 4
            ]
        }
        result = self.client.post(reverse('menu-add'), data=data_to_add)
        self.assertEqual(result.status_code, 401)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + self.token.key)
        result = self.client.post(reverse('menu-add'), data=data_to_add)
        self.assertEqual(result.status_code, 201)

    def test__menu_update_authorization(self):
        data_to_update = {
            "name": "Kuchnia Gruzińska",
            "description": "Kuchnia Gruzińska",
            "dishes": [
                1, 2
            ]
        }
        result = self.client.put(reverse('menu-update', kwargs={'pk': 1}), data_to_update,
                                 content_type='application/json')
        self.assertEqual(result.status_code, 401)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + self.token.key)
        result = self.client.put(reverse('menu-update', kwargs={'pk': 1}), data_to_update,
                                 content_type='application/json')
        self.assertEqual(result.status_code, 200)

    def test__menu_destroy_authorization(self):
        result = self.client.delete(reverse('menu-destroy', kwargs={'pk': 1}))
        self.assertEqual(result.status_code, 401)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + self.token.key)
        result = self.client.delete(reverse('menu-destroy', kwargs={'pk': 1}))
        self.assertEqual(result.status_code, 204)

    def test__wrong_credentials(self):
        wrong_data = {"username": "notexists", "password": "notexists"}
        token = self.client.post(reverse('api_token_auth'), wrong_data)
        self.assertEqual(token.status_code, 400)

