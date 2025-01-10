from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from authentication.models import Tier
from ..models import Payment
from .serializer import PaymentSerializer
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):  
    permission_classes = [permissions.IsAuthenticated]   
    def post(self, request, price_id):
        try:
            PRICE_TIER_MAP = {
                'price_1QdwivRZZTayXP3ZAb0BM0ry': {'tier': Tier.BASIC, 'amount': 15.00},
                'price_1QdwsJRZZTayXP3ZRTlV52rk': {'tier': Tier.PREMIUM, 'amount': 100.00}
            }

            if price_id not in PRICE_TIER_MAP:
                return Response(
                    {'error': 'Invalid price ID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    }
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url = settings.SITE_URL + '/payment-success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = settings.SITE_URL + '/payment-canceled',
            )

            Payment.objects.create(
                user=request.user,
                stripe_session_id=checkout_session.id,
                amount=PRICE_TIER_MAP[price_id]['amount'],
                price_id=price_id,
                status='pending'
            )

            return Response(
                {'url': checkout_session.url},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
class PaymentSuccessView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        session_id = request.query_params.get('session_id')
        
        if not session_id:
            return Response(
                {'error': 'No session ID provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Retrieve the session from Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Check if payment was successful
            if session.payment_status == 'paid':
                # Get the payment record
                payment = Payment.objects.get(stripe_session_id=session_id)
                
                if payment.status != 'completed':
                    # Update payment status
                    payment.status = 'completed'
                    payment.save()

                    # Update user's tier based on the price_id
                    PRICE_TIER_MAP = {
                        'price_1QdwivRZZTayXP3ZAb0BM0ry': Tier.BASIC,
                        'price_1QdwsJRZZTayXP3ZRTlV52rk': Tier.PREMIUM
                    }
                    
                    user = request.user
                    user.tier = PRICE_TIER_MAP[payment.price_id]
                    user.save()

                return Response({
                    'status': 'success',
                    'message': 'Payment completed successfully'
                })
            
            return Response({
                'status': 'error',
                'message': 'Payment not completed'
            }, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response({
                'error': 'Payment record not found'
            }, status=status.HTTP_404_NOT_FOUND)
        

class PaymentsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)