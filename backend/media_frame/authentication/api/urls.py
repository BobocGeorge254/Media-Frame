# authentication/api/urls.py
from django.urls import path
from .views import ConfirmEmailView, ForgotPasswordView, ResetPasswordView, UserRegisterView, UserLoginView, UserLogoutView, UserDetailView, UserUpdateView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name="reset-password"),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:user_id>/update/', UserUpdateView.as_view(), name='user-update'),
    path('confirm-email/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirm-email'),

]
