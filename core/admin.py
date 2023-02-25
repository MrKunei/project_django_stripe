from django.contrib import admin
from core.models import Item, Discount, Tax, Order


@admin.register(Item)
class AdminItem(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name',)


@admin.register(Discount)
class AdminDiscount(admin.ModelAdmin):
    list_display = ('name', 'percent_off',)


@admin.register(Tax)
class AdminTax(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'inclusive',)


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('id', 'discount', 'tax',)
