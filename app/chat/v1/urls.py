from django.urls import path

app_name = 'chat'

from chat.v1.views.chat_view import CreateChatView


urlpatterns = [
    path('create/<str:username>/', CreateChatView.as_view(), name='create-chat')
]
