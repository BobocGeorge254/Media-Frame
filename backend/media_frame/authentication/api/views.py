from authentication.models import CustomUser
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate 

class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate token and send email confirmation
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_url = f"http://127.0.0.1:3000/confirm-email/{uid}/{token}/"

            send_mail(
                subject="Email Confirmation",
                message=f"Click the link to confirm your email: {confirm_url}",
                from_email="noreply@mediaframe.com",
                recipient_list=[user.email],
            )

            return Response({'message': 'User created successfully! Please confirm your email.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ConfirmEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(CustomUser, pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_email_confirmed = True
                user.save()
                return Response({"message": "Email confirmed successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = []  # Allow any user to access this view

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_email_confirmed:
            return Response(
                {"error": "Email not confirmed. Please check your email."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]  
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"http://127.0.0.1:3000/reset-password/{uid}/{token}/"

            # Send reset email
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link below to reset your password:\n{reset_url}",
                from_email="noreply@mediaframe.com",
                recipient_list=[user.email],
            )
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "No account found with this email address."}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(CustomUser, pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            password = request.data.get("password")
            if not password:
                return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)
        

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):

        if request.user.id != user_id:
            return Response(
                {"error": "You are not authorized to access this user's details."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user = CustomUser.objects.get(id=user_id)
        user_data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "tier": user.tier,
            "date_joined": user.date_joined,
        }
        return Response(user_data, status=status.HTTP_200_OK)
    

class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_id):
        # Check if the user trying to update their details is the correct user
        if request.user.id != user_id:
            return Response(
                {"error": "You are not authorized to update this user's details."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Fetch the user object
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Validate the data passed in the request body
        data = request.data

        # You can allow the user to update specific fields (for example: tier, first_name, last_name, etc.)
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.save()

        return Response(
            {"message": "User details updated successfully."},
            status=status.HTTP_200_OK,
        )
