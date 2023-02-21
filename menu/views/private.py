from ..models import Dish, DishMenu, Menu
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from ..serializers import DishSerializer, PrivateMenuSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import json
from rest_framework import generics
from django.utils import timezone


class MenuCreateAPIView(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = PrivateMenuSerializer
    permission_classes = (IsAuthenticated,)


class DishCreateAPIView(generics.CreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = (IsAuthenticated,)


class MenuUpdateApiView(generics.UpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = PrivateMenuSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        instance = serializer.save(last_modification=timezone.now())


class DishUpdateApiView(generics.UpdateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        instance = serializer.save(last_modification=timezone.now())


class MenuDestroyApiView(generics.DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = PrivateMenuSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class DishDestroyApiView(generics.DestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
