from django.contrib import admin
from .models import *

class PersonAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'last_name', 'phone_num', 'is_active', 'is_staff')
    search_fields = ('email', 'name', 'last_name', 'phone_num')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'last_name', 'phone_num', 'reset_password_token')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'last_name', 'phone_num', 'is_active', 'is_staff')}
        ),
    )
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Person2, PersonAdmin)

class UserSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'phone_num', 'email', 'status')
    search_fields = ('name', 'last_name', 'phone_num', 'email')
    list_filter = ('status',)
    ordering = ('name',)

admin.site.register(UserSite2, UserSiteAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Category2, CategoryAdmin)

class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Promocode, PromocodeAdmin)

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Unit2, UnitAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_new', 'discount')
    search_fields = ('name', 'category__name', 'description')
    list_filter = ('category', 'is_new', 'discount')
    ordering = ('name',)

admin.site.register(Product2, ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'siteuser', 'total_price', 'is_accepted', 'is_payed', 'status')
    search_fields = ('person__email', 'siteuser__name', 'siteuser__last_name', 'address')
    list_filter = ('is_accepted', 'is_payed', 'status')
    ordering = ('-created_at',)

admin.site.register(Cart2, CartAdmin)


admin.site.register(Poster)
admin.site.register(Pay_on_delivery)