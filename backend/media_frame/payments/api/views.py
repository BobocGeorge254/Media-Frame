from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):  
    permission_classes = [permissions.AllowAny]   
    def post(self, request, price_id):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    }
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url = settings.SITE_URL+ '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url = settings.SITE_URL + '?canceled=true',
            )


            return redirect(checkout_session.url)

        except:
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )