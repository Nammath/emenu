from rest_framework import serializers
from .models import Dish, DishMenu, Menu


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            'name',
            'description',
            'price',
            'preparation_time',
            'is_vegetarian'
        ]


class PublicMenuSerializer(serializers.ModelSerializer):
    num_dishes = serializers.IntegerField(source='dishes.count', read_only=True)
    dishes = DishSerializer(read_only=True, many=True)

    class Meta:
        model = Menu
        fields = [
            'name',
            'description',
            'num_dishes',
            'dishes',
        ]


class PrivateMenuSerializer(serializers.ModelSerializer):
    dishes = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), write_only=True, many=True)

    class Meta:
        model = Menu
        fields = [
            'name',
            'description',
            'dishes',
        ]
        extra_kwargs = {'dishes': {'required': False}}


class DishMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishMenu
        fields = '__all__'
