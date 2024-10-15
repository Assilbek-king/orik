from django.http import JsonResponse

from .models import *
from .serializers import PromocodeSerializer, CategorySerializer, ProductSerializer, CartSerializer,PersonSerializer, LoginSerializer, ResetPasswordSerializer,PosterSerializer,PayOnDeliverySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import secrets
from rest_framework.authtoken.models import Token
import requests
import os
from django.conf import settings

import requests
from django.http import JsonResponse
from django.conf import settings



import requests
from django.http import JsonResponse


def suggest_view(request):
    query = request.GET.get('query', '')
    url = "https://catalog.api.2gis.ru/3.0/suggests"
    params = {
        "key": settings.DGIS_API_KEY,
        "q": query,
        "viewpoint1": "69.20251452558023,42.39648259337066",
        "viewpoint2": "69.97155747441977,42.23440940662934",
        # Минимальный набор полей для сокращения объема данных
        "fields": "items.name_ex,items.address_name,items.type,items.point",
        "type": "branch,building",
        "search_device_type": "desktop",
        "search_user_hash": "7005176812676539700",
        "locale": "ru_KZ",
        "stat[sid]": "367503b7-37b7-4996-b5b0-daf647959b23",
        "stat[user]": "4ec42c7a-a751-49ba-87e3-0ecdbe003804",
        "shv": "2024-10-07-20",
        "r": "119935042"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)



class CalculateDistanceView(APIView):
    def post(self, request, *args, **kwargs):
        origin = request.data.get('origin', '')  # Получаем точку отправления
        destination = '42.366991,69.52625'  # Фиксированная точка назначения
        mode = 'driving'  # Режим по умолчанию
        api_key = 'AIzaSyDqiZx9bv1VK85IzCLSeXy9FvCjZeB-_bc'  # Получаем ключ API из переменных окружения

        if not origin:
            return Response({'error': 'Точка отправления не указана.'}, status=status.HTTP_400_BAD_REQUEST)

        if not api_key:
            return Response({'error': 'API ключ не найден.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = 'https://maps.googleapis.com/maps/api/directions/json'
        params = {
            'origin': origin,
            'destination': destination,
            'mode': mode,
            'key': api_key
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data['status'] == 'OK':
                route = data['routes'][0]
                legs = route['legs'][0]
                distance = legs['distance']['text']
                duration = legs['duration']['text']
                steps = [step['html_instructions'] for step in legs['steps']]

                return Response({
                    'distance': distance,
                    'duration': duration,
                })

            else:
                return Response({'error': 'Маршрут не найден.'}, status=status.HTTP_400_BAD_REQUEST)

        except requests.RequestException as e:
            return Response({'error': f'Ошибка запроса: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PayOnDeliveryAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                pay_delivery = Pay_on_delivery.objects.get(pk=pk)
            except Pay_on_delivery.DoesNotExist:
                return Response({'error': 'Pay_on_delivery record not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PayOnDeliverySerializer(pay_delivery)
        else:
            pay_deliveries = Pay_on_delivery.objects.all()
            serializer = PayOnDeliverySerializer(pay_deliveries, many=True)
        return Response(serializer.data)




class CheckPromocodeView(APIView):
    def post(self, request, *args, **kwargs):
        promocode_name = request.data.get('name')
        try:
            promocode = Promocode.objects.get(name=promocode_name, status=True)
            serializer = PromocodeSerializer(promocode)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Promocode.DoesNotExist:
            return Response({'error': 'Invalid promocode or inactive'}, status=status.HTTP_400_BAD_REQUEST)


class SignupAPIView(APIView):
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': PersonSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': PersonSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ResetPasswordAPIView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"detail": "Password reset code has been sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserLocationAPIView(APIView):
#     def post(self, request, format=None):
#         serializer = UserLocationSerializer(data=request.data)
#         if serializer.is_valid():
#             latitude = serializer.validated_data.get('latitude')
#             longitude = serializer.validated_data.get('longitude')
#
#             # Здесь можно сохранить координаты в базу данных или выполнить другие действия
#             # Например:
#             # request.user.profile.latitude = latitude
#             # request.user.profile.longitude = longitude
#             # request.user.profile.save()
#
#             return Response({'message': 'Координаты успешно сохранены'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                category = Category2.objects.get(pk=pk)
            except Category2.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CategorySerializer(category)
        else:
            categories = Category2.objects.all()
            serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            category = Category2.objects.get(pk=pk)
        except Category2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category2.objects.get(pk=pk)
        except Category2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PosterAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                category = Poster.objects.get(pk=pk)
            except Poster.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = PosterSerializer(category)
        else:
            categories = Poster.objects.all()
            serializer = PosterSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PosterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            category = Poster.objects.get(pk=pk)
        except Poster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PosterSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Poster.objects.get(pk=pk)
        except Poster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                product = Product2.objects.get(pk=pk)
            except Product2.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            products = Product2.objects.all()
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(result_page, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            product = Product2.objects.get(pk=pk)
        except Product2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product2.objects.get(pk=pk)
        except Product2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartAPIView(APIView):
    def get(self, request, pk=None):
        person_id = request.query_params.get('person_id', None)  # Получаем person_id из параметров запроса

        if pk:
            try:
                cart = Cart2.objects.get(pk=pk)
            except Cart2.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CartSerializer(cart)
        elif person_id:
            # Фильтрация корзин по person_id
            carts = Cart2.objects.filter(person_id=person_id)
            if not carts.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CartSerializer(carts, many=True)
        else:
            carts = Cart2.objects.all()
            serializer = CartSerializer(carts, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            cart = Cart2.objects.get(pk=pk)
        except Cart2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            cart = Cart2.objects.get(pk=pk)
        except Cart2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                person = Person2.objects.get(pk=pk)
                serializer = PersonSerializer(person)
                return Response(serializer.data)
            except Person2.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            persons = Person2.objects.all()
            serializer = PersonSerializer(persons, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            person = Person2.objects.get(pk=pk)
            serializer = PersonSerializer(person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Person2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            person = Person2.objects.get(pk=pk)
            person.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Person2.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
