from django.contrib import admin
from main.models import *
# Register your models here.

admin.site.register(Person)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishItem)
