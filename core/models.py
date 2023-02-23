from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):

    class Currency(models.TextChoices):
        USD = 'usd', 'usd'
        RUB = 'rub', 'rub'

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.PositiveIntegerField(default=1, help_text='price in dollars cents')
    currency = models.CharField(choices=Currency.choices, max_length=3, default=Currency.USD)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Discount(models.Model):
    name = models.CharField(max_length=100, null=True)
    percent_off = models.PositiveIntegerField(default=0)


class Tax(models.Model):

    name = models.CharField(max_length=100, null=True)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    inclusive = models.BooleanField(default=False)


class Order(models.Model):

    class Currency(models.TextChoices):
        USD = 'usd', 'usd'
        RUB = 'rub', 'rub'

    items = models.ManyToManyField(Item, related_name='order')
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, related_name='order')
    tax = models.ForeignKey(Tax, on_delete=models.PROTECT, related_name='order')
    currency = models.CharField(choices=Currency.choices, max_length=3, default=Currency.USD)
