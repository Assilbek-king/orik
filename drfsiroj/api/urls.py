from django.urls import path
from .views import (
    CategoryAPIView,
    ProductAPIView,
    CartAPIView,
    PersonAPIView,
    ResetPasswordAPIView,
    PosterAPIView,
    CheckPromocodeView,
    CalculateDistanceView,
    suggest_view,
    PayOnDeliveryAPIView

)
from .views import SignupAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('search_address/', suggest_view, name='autocomplete_address'),
    path('pay_on_delivery/', PayOnDeliveryAPIView.as_view(), name='PayOnDeliveryViewSet'),

    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),

    path('categories/', CategoryAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryAPIView.as_view(), name='category-detail'),

    path('products/', ProductAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product-detail'),

    path('carts/', CartAPIView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartAPIView.as_view(), name='cart-detail'),

    path('persons/', PersonAPIView.as_view(), name='person-list'),
    path('persons/<int:pk>/', PersonAPIView.as_view(), name='person-detail'),

    path('posters/', PosterAPIView.as_view(), name='poster-list'),
    path('posters/<int:pk>/', PosterAPIView.as_view(), name='poster-detail'),

    path('check-promocode/', CheckPromocodeView.as_view(), name='check-promocode'),
    path('calculate_distance/', CalculateDistanceView.as_view(), name='calculate_distance'),

]
