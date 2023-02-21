from django.db import models
from django.db.models import Count


class Dish(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_time = models.TimeField()
    added_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now_add=True)
    is_vegetarian = models.BooleanField()

    def __str__(self):
        return self.name


class MenuQuerySet(models.QuerySet):
    def search(self, name, date_added_start, date_added_finish, date_modified_start, date_modified_finish):
        qs = self.annotate(num_dishes=Count('dishes')).filter(num_dishes__gt=0)

        if name:
            qs = qs.filter(name__icontains=name)
        if date_added_start and date_added_finish:
            qs = qs.filter(added_date__range=[date_added_start, date_added_finish])
        if date_modified_start and date_modified_finish:
            qs = qs.filter(last_modification__range=[date_modified_start, date_modified_finish])

        return qs


class MenuManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return MenuQuerySet(self.model, using=self._db)

    def search(self, name, date_added_start, date_added_finish, date_modified_start, date_modified_finish):
        return self.get_queryset().search(name, date_added_start, date_added_finish, date_modified_start,
                                          date_modified_finish)


class Menu(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField(blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now_add=True)
    dishes = models.ManyToManyField(Dish, related_name='menus', through='DishMenu')

    objects = MenuManager()

    def __str__(self):
        return self.name


class DishMenu(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
