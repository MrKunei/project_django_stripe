from django.urls import path
from core.views import ListItemsView, DetailItemView, CreateCheckoutSessionView, SuccessView, CancelView

urlpatterns = [
    path('', ListItemsView.as_view(), name='list_items'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('item/<int:pk>/', DetailItemView.as_view(), name='detail_item'),
    path('buy/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session')
]