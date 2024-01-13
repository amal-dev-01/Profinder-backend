# websocket_urlpatterns = [
#     # path('ws/chat/', ChatConsumer.as_asgi())
# ]


# import app.routing
# from django.urls import re_path,path
# from chat.consumers import TextRoomConsumer
# websocket_urlpatterns = [
#     re_path(r"ws/(?P<room_name>\w+)/$", TextRoomConsumer.as_asgi()),
#     # path('ws/<str:room_name>/', TextRoomConsumer.as_asgi()),

# ]

# from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]
