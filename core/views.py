import stripe
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from .models import Item


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

    def get_object(self):
        return Item.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs['pk'])
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
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
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

