from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Menu, DishMenu
from django.db.models import Count
from rest_framework.authtoken.models import Token
from django.test import Client

User = get_user_model()


class MenuTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@test.pl', 'test')
        self.client.login(username='test', password='test')
        self.token, created = Token.objects.get_or_create(user=self.user)

    def test_details(self):
        menu = Menu.objects.first()
        result = self.client.get(reverse('menu_detail', kwargs={'pk': menu.pk})).json()
        self.assertEqual(result['name'], menu.name)
        dishes_count = DishMenu.objects.filter(menu=menu).count()
        self.assertEqual(dishes_count, len(result["dishes"]))

    def test_list(self):
        menu_count_all = Menu.objects.all()
        menu_count = Menu.objects.annotate(num_dishes=Count('dishes')).filter(num_dishes__gt=0).count()
        result = self.client.get(reverse('menu_list')).json()
        self.assertNotEqual(menu_count_all, len(result))
        self.assertEqual(menu_count, len(result))

    def test_list_ordering_num_dishes(self):
        ordering_data = {"ordering": "num_dishes"}
        result = self.client.get(reverse('menu_list'), data=ordering_data).json()
        dish_counts = [menu["num_dishes"] for menu in result]
        self.assertEqual(dish_counts, sorted(dish_counts))
        ordering_data = {"ordering": "-num_dishes"}
        result = self.client.get(reverse('menu_list'), data=ordering_data).json()
        dish_counts = [menu["num_dishes"] for menu in result]
        self.assertEqual(dish_counts, sorted(dish_counts, reverse=True))

    def test_list_ordering_name(self):
        ordering_data = {"ordering": "name"}
        result = self.client.get(reverse('menu_list'), data=ordering_data).json()
        names = [menu["name"] for menu in result]
        self.assertEqual(names, sorted(names))
        ordering_data = {"ordering": "-name"}
        result = self.client.get(reverse('menu_list'), data=ordering_data).json()
        names = [menu["name"] for menu in result]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_list_name_contains(self):
        filter_param = "Wło"
        menu_count = Menu.objects.filter(name__icontains=filter_param).count()
        filter_params = {"name": filter_param}
        result = self.client.get(reverse('menu_list'), data=filter_params).json()
        self.assertEqual(len(result), menu_count)

    def test_list_date_added(self):
        date_range = ["2023-02-19", "2023-02-20"]
        filter_params = {
            "date_added_start": date_range[0],
            "date_added_finish": date_range[1]
        }
        menu_count = Menu.objects.filter(added_date__range=date_range).count()
        result = self.client.get(reverse('menu_list'), data=filter_params).json()
        self.assertEqual(len(result), menu_count)

    def test_list_date_modified(self):
        date_range = ["2023-02-19", "2023-02-20"]
        filter_params = {
            "date_modified_start": date_range[0],
            "date_modified_finish": date_range[1]
        }
        menu_count = Menu.objects.filter(last_modification__range=date_range).count()
        result = self.client.get(reverse('menu_list'), data=filter_params).json()
        self.assertEqual(len(result), menu_count)

    def test_add_menu(self):
        data = {
            "name": "Kuchnia Bułgarska",
            "description": "Kuchnia Bułgarska",
            "dishes": [1]
        }
        self.client = Client(HTTP_AUTHORIZATION='Token ' + self.token.key)
        result = self.client.post(reverse('menu-add'), data=data)
        self.assertEqual(result.status_code, 201)
        menu = Menu.objects.last()
        self.assertEqual(menu.name, "Kuchnia Bułgarska")

    def test_update_menu(self):
        menu = Menu.objects.last()
        menu_last_modification = menu.last_modification
        data = {
            "name": "Kuchnia Albańska",
            "description": "Kuchnia Albańska",
            "dishes": [2]
        }
        self.client = Client(HTTP_AUTHORIZATION='Token ' + self.token.key)
        result = self.client.put(reverse('menu-update', kwargs={'pk': menu.pk}), data=data,
                                 content_type='application/json')
        self.assertEqual(result.status_code, 200)
        menu = Menu.objects.last()
        menu_last_modification_new = menu.last_modification
        self.assertNotEqual(menu_last_modification, menu_last_modification_new)

    def test_delete_menu(self):
        menu = Menu.objects.last()
        menu_pk = menu.pk
        self.client = Client(HTTP_AUTHORIZATION='Token ' + self.token.key)
        result = self.client.delete(reverse('menu-destroy', kwargs={'pk': menu_pk}))
        self.assertEqual(result.status_code, 204)
        menu = Menu.objects.last()
        menu_pk_new = menu.pk
        self.assertNotEqual(menu_pk, menu_pk_new)
