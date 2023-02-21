from django.urls import path
from .views.public import MenuListAPIView, MenuDetailApiView, DishDetailApiView, DishListAPIView
from .views.private import MenuCreateAPIView, DishCreateAPIView, MenuUpdateApiView, DishUpdateApiView, \
    MenuDestroyApiView, DishDestroyApiView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu/list', MenuListAPIView.as_view(), name="menu_list"),
    path('menu/<int:pk>/detail', MenuDetailApiView.as_view(), name="menu_detail"),
    path('menu/add', MenuCreateAPIView.as_view(), name='menu-add'),
    path('menu/<int:pk>/update', MenuUpdateApiView.as_view(), name='menu-update'),
    path('menu/<int:pk>/destroy', MenuDestroyApiView.as_view(), name='menu-destroy'),
    path('dish/list', DishListAPIView.as_view(), name="dish_list"),
    path('dish/<int:pk>/detail', DishDetailApiView.as_view(), name="dish_detail"),
    path('dish/<int:pk>/destroy', DishDestroyApiView.as_view(), name='dish-destroy'),
    path('dish/<int:pk>/update', DishUpdateApiView.as_view(), name='dish-update'),
    path('dish/add', DishCreateAPIView.as_view(), name='dish-add'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]