from django.urls import path
from .views import StripeCheckoutView

urlpatterns = [
    path('stripe-checkout/<str:price_id>/', StripeCheckoutView.as_view(), name='stripe-checkout'),
]