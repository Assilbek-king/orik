from django.db import models
from datetime import datetime

class Person(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_num = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserSite(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_num = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='upload', blank=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image1 = models.ImageField(upload_to='upload')
    price = models.IntegerField(default=0)
    compound = models.TextField(blank=True)
    country = models.CharField(max_length=100,blank=True)
    discount = models.IntegerField(default=0)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class Cart(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    siteuser = models.ForeignKey(UserSite, on_delete=models.CASCADE,blank=True,null=True)
    address = models.CharField(max_length=200, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    pr_count = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)

    order = models.TextField()

    created_at = models.DateTimeField(default=datetime.now)
    finished_at = models.DateTimeField(default=datetime.now)
    status = models.IntegerField(default=0)  # 0 - created zakaz, -1 - otmenen, 1 - confirmed, 2 - accepted



    def __str__(self):
        return f'Cart {self.id} for {self.person.name} {self.person.last_name}'

