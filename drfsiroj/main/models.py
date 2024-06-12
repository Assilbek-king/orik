from django.db import models
from datetime import datetime
class Person(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_num = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200)
    location = models.TextField(blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class SiteUser(models.Model):
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
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image1 = models.ImageField(upload_to='upload')
    image2 = models.ImageField(upload_to='upload', blank=True)
    image3 = models.ImageField(upload_to='upload', blank=True)
    price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0, blank=True)
    compound = models.TextField(blank=True)
    storage_cond = models.TextField(blank=True)
    country = models.CharField(max_length=100,blank=True)
    discount = models.IntegerField(default=0)
    is_new = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0, blank=True)

    def __str__(self):
        return self.name




class Cart(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    siteuser = models.ForeignKey(SiteUser, on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    status = models.IntegerField(default=0)  # 0 - created zakaz, -1 - otmenen, 1 - confirmed, 2 - accepted
    amount = models.FloatField(default=0)
    orig_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    finished_at = models.DateTimeField(default=datetime.now)



    def __str__(self):
        return f'Cart {self.id} for {self.person.name} {self.person.last_name}'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    price = models.FloatField(default=0)
    status = models.IntegerField(default=0)  # 0 - created, -1 - deleted
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f'CartItem {self.id} for Cart {self.cart.id}: {self.product.name} - {self.amount}'


class WishItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)

    def _str_(self):
        return f'{self.person.id} {self.good.title}'