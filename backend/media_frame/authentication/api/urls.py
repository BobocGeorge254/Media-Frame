from django.urls import path
from .views import ConfirmEmailView, ForgotPasswordView, ResetPasswordView, UserRegisterView, UserLoginView, UserLogoutView, UserDetailView, UserDeleteSelfView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('delete-account/', UserDeleteSelfView.as_view(), name='delete_account'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name="reset-password"),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('confirm-email/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
