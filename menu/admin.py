from django.contrib import admin
from .models import Dish, Menu, DishMenu

admin.site.register(Dish)
admin.site.register(Menu)
admin.site.register(DishMenu)
