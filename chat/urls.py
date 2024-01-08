from django.urls import path
from chat.views import  ListUser




urlpatterns = [
    path("chat/", ListUser.as_view(), name="chat"),
]


