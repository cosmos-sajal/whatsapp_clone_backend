from django.urls import path

from user.v1.views.user_view import RegisterUserView
from user.v1.views.otp_view import OTPGenerateView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('otp/generate/', OTPGenerateView.as_view(), name='generate-otp'),
]
