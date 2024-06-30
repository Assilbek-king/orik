from api.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from django.core.mail import send_mail
import secrets

Person = get_user_model()


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person2
        fields = ('id', 'email', 'name', 'last_name', 'phone_num', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Person2.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'")

        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = Person2.objects.get(email=value)
            # Generate a 6-digit random code
            reset_code = ''.join(secrets.choice('0123456789') for i in range(6))
            user.reset_password_token = reset_code
            user.save()

            # Send email with the reset code
            send_mail(
                'Password Reset Code',
                f'Your password reset code: {reset_code}',
                'from@example.com',
                [value],
                fail_silently=False,
            )

            return value
        except Person2.DoesNotExist:
            raise serializers.ValidationError("User does not exist")


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit2
        fields = ('name',)

class ProductSerializer(serializers.ModelSerializer):
    unit = serializers.StringRelatedField()

    class Meta:
        model = Product2
        fields = ('id', 'category', 'name', 'description', 'image1', 'price',
                  'compound', 'storage', 'unit', 'country', 'discount', 'is_new')

    def create(self, validated_data):
        unit_data = validated_data.pop('unit', None)
        if unit_data:
            unit, created = Unit2.objects.get_or_create(name=unit_data)
            validated_data['unit'] = unit
        return Product2.objects.create(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category2
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart2
        fields = '__all__'


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = '__all__'



