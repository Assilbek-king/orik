from django.urls import path
from .views import (
    CategoryAPIView,
    ProductAPIView,
    CartAPIView,
    PersonAPIView,

)
from .views import SignupAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    path('categories/', CategoryAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryAPIView.as_view(), name='category-detail'),

    path('products/', ProductAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product-detail'),

    path('carts/', CartAPIView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartAPIView.as_view(), name='cart-detail'),

    path('persons/', PersonAPIView.as_view(), name='person-list'),
    path('persons/<int:pk>/', PersonAPIView.as_view(), name='person-detail'),

]
