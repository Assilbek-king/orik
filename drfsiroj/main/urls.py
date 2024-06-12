from django.urls import path

from main.views import *

urlpatterns = [
    path('persons/', PersonList.as_view()),
    path('persons/<int:pk>/', PersonDetail.as_view()),

    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),

    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', ProductDetail.as_view()),

    path('carts/', CartList.as_view()),
    path('carts/<int:pk>/', CartDetail.as_view()),

    path('cartitems/', CartItemList.as_view()),
    path('cartitems/<int:pk>/', CartItemDetail.as_view()),

    path('wishitems/', WishItemList.as_view()),
    path('wishitems/<int:pk>/', WishItemDetail.as_view()),
]
