from django.urls import path

from user.v1.views.user_view import RegisterUserView, VerifyEmailView
from user.v1.views.otp_view import OTPGenerateView, OTPValidateView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('otp/generate/', OTPGenerateView.as_view(), name='generate-otp'),
    path('otp/validate/', OTPValidateView.as_view(), name='validate-otp'),
    path('email/verify/', VerifyEmailView.as_view(), name='verify-email')
]
