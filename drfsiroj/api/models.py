from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
import secrets


class PersonManager(BaseUserManager):
    def create_user(self, phone_num, password=None, **extra_fields):
        if not phone_num:
            raise ValueError('Phone number is required')
        user = self.model(phone_num=phone_num, **extra_fields)
        user.set_password(password)  # Пароль шифруется
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_num, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_num, password, **extra_fields)

class Person2(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    phone_num = models.CharField(max_length=200, unique=True)  # Убедитесь, что поле уникально

    reset_password_token = models.CharField(max_length=6, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = PersonManager()

    USERNAME_FIELD = 'phone_num'  # Используем телефонный номер в качестве основного поля для логина
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_num  # Возвращаем номер телефона в строковом представлении



class UserSite2(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_num = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Promocode(models.Model):
    name = models.CharField(max_length=200)
    discount = models.IntegerField(blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Category2(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='upload', blank=True)

    def __str__(self):
        return self.name


class Unit2(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product2(models.Model):
    category = models.ForeignKey(Category2,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image1 = models.ImageField(upload_to='upload')
    price = models.IntegerField(default=0)
    compound = models.TextField(blank=True)
    storage = models.TextField(blank=True)
    unit = models.ForeignKey(Unit2, on_delete=models.CASCADE, blank=True,null=True)
    country = models.CharField(max_length=100,blank=True)
    discount = models.IntegerField(default=0)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Poster(models.Model):
    name = models.CharField(max_length=300, default='yozma hech narsa',blank=True)
    image = models.ImageField(upload_to='upload')

    def __str__(self):
        return self.name


class Cart2(models.Model):
    person = models.ForeignKey(Person2, on_delete=models.CASCADE)
    siteuser = models.ForeignKey(UserSite2, on_delete=models.CASCADE,blank=True,null=True)
    address = models.CharField(max_length=200, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    pr_count = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)

    order = models.TextField()

    created_at = models.DateTimeField(default=datetime.now)
    finished_at = models.DateTimeField(default=datetime.now)
    status = models.IntegerField(default=1)  # 0 - created zakaz, -1 - otmenen, 1 - confirmed, 2 - accepted



    def __str__(self):
        return f'Cart {self.id} for {self.person.name} {self.person.last_name}'



class Pay_on_delivery(models.Model):
    price_for_car = models.IntegerField(default=120,blank=True)
    price_for_maped = models.IntegerField(default=70,blank=True)
    limit = models.IntegerField(default=6,blank=True)

    def __str__(self):
        return str(self.price_for_car)
