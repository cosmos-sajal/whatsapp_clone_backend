from django.urls import path

from user.v1.views.user_view import RegisterUserView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user')
]
