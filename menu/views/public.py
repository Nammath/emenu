from ..models import Menu, Dish
from ..serializers import PublicMenuSerializer, DishSerializer
from rest_framework import generics
from rest_framework import filters


class MenuListAPIView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = PublicMenuSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'num_dishes']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        name = self.request.GET.get('name')
        date_added_start = self.request.GET.get('date_added_start')
        date_added_finish = self.request.GET.get('date_added_finish')
        date_modified_start = self.request.GET.get('date_modified_start')
        date_modified_finish = self.request.GET.get('date_modified_finish')
        result = qs.search(name, date_added_start, date_added_finish, date_modified_start, date_modified_finish)
        return result


class MenuDetailApiView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Menu.objects.all()
    serializer_class = PublicMenuSerializer


class DishListAPIView(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishDetailApiView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
