from django.contrib import admin
from core.models import Item


@admin.register(Item)
class AdminItem(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name',)
