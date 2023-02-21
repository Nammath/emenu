from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Dish
from django.db.models import Count
from rest_framework.authtoken.models import Token
from django.test import Client

User = get_user_model()


class DishTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@test.pl', 'test')
        self.client.login(username='test', password='test')
        self.token, created = Token.objects.get_or_create(user=self.user)

    def test_details(self):
        dish = Dish.objects.first()
        result = self.client.get(reverse('dish_detail', kwargs={'pk': dish.pk})).json()
        self.assertEqual(result['name'], dish.name)

    def test_add_dish(self):
        data = {
            "name": "Kotlet",
            "description": "Kotlet mielony",
            "price": 19.99,
            "preparation_time": "0:30:20",
        }
        self.client = Client(HTTP_AUTHORIZATION='Token ' + self.token.key)
        result = self.client.post(reverse('dish-add'), data=data)
        self.assertEqual(result.status_code, 201)
        dish = Dish.objects.last()
        self.assertEqual(dish.name, "Kotlet")

    def test_update_dish(self):
        dish = Dish.objects.last()
        dish_last_modification = dish.last_modification
        data = {
            "name": "Ryba",
            "description": "Ryba po grecku",
            "price": 29.99,
            "preparation_time": "0:10:10",
            "is_vegetarian": False
        }
        self.client = Client(HTTP_AUTHORIZATION='Token ' + self.token.key)
        result = self.client.put(reverse('dish-update', kwargs={'pk': dish.pk}), data=data,
                                 content_type='application/json')
        self.assertEqual(result.status_code, 200)
        dish = Dish.objects.last()
        dish_last_modification_new = dish.last_modification
        self.assertNotEqual(dish_last_modification, dish_last_modification_new)

    def test_delete_dish(self):
        dish = Dish.objects.last()
        dish_pk = dish.pk
        self.client = Client(HTTP_AUTHORIZATION='Token ' + self.token.key)
        result = self.client.delete(reverse('dish-destroy', kwargs={'pk': dish_pk}))
        self.assertEqual(result.status_code, 204)
        dish = Dish.objects.last()
        dish_pk_new = dish.pk
        self.assertNotEqual(dish_pk, dish_pk_new)
