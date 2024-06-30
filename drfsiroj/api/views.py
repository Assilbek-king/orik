from .models import *
from .serializers import CategorySerializer, ProductSerializer, CartSerializer,PersonSerializer, LoginSerializer, ResetPasswordSerializer,PosterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import secrets
from rest_framework.authtoken.models import Token

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
        else:
            products = Product2.objects.all()
            serializer = ProductSerializer(products, many=True)
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
        if pk:
            try:
                cart = Cart2.objects.get(pk=pk)
            except Cart2.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CartSerializer(cart)
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
