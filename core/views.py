import os

import stripe
from django.db.models import Sum
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class ListItemsView(ListView):
    queryset = Item.objects.all()
    template_name = 'core/list_items.html'


class SuccessView(TemplateView):
    template_name = "core/success.html"


class CancelView(TemplateView):
    template_name = 'core/cancel.html'


class DetailItemView(DetailView):
    template_name = 'core/detail_item.html'

    def get_object(self, queryset=None):
        return Item.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs['pk'])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'unit_amount': item.price,
                    'product_data': {
                        'name': item.name,
                    },
                },
                'quantity': 1,
                },
            ],
            metadata={
                "product_id": item.id
            },
            mode='payment',
            success_url=os.environ.get('DOMAIN') + '/success/',
            cancel_url=os.environ.get('DOMAIN') + '/cancel/',
        )
        return JsonResponse({'id': checkout_session.id})


class OrderView(DetailView):
    template_name = 'core/detail_order.html'

    def get_object(self, queryset=None):
        return Order.objects.get(id=self.kwargs['pk']).select_related('discount', 'tax').prefetch_related('item').first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.items.all()
        unit_amount = items.aggregate(unit_amount=Sum('price'))['unit_amount']
        context.update({
            'items': items,
            'unit_amount': unit_amount,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateOrderCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk']).select_related('discount', 'tax').prefetch_related('item').first()
        items = order.items.all()
        discounts = []
        if order.discount:
            coupon = stripe.Coupon.create(percent_off=order.discount.percent_off)
            discounts = [{'coupon': f'{coupon.id}', }]
        tax = stripe.TaxRate.create(
            display_name=order.tax.name,
            inclusive=order.tax.inclusive,
            percentage=order.tax.percentage,
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'unit_amount': item.price,
                    'product_data': {
                        'name': item.name,
                    },
                },
                'quantity': 1,
                'tax_rates': [tax['id']]
            }for item in items],
            mode='payment',
            discounts=discounts,
            success_url=os.environ.get('DOMAIN') + '/success/',
            cancel_url=os.environ.get('DOMAIN') + '/cancel/',
        )
        return JsonResponse({'id': checkout_session.id})
