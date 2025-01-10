from django.urls import path
from .views import StripeCheckoutView, PaymentSuccessView, PaymentsAPIView

urlpatterns = [
    path('stripe-checkout/<str:price_id>/', StripeCheckoutView.as_view(), name='stripe-checkout'),
    path('payment-success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('', PaymentsAPIView.as_view(), name='payments')
]