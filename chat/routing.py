

# websocket_urlpatterns = [
#     # path('ws/chat/', ChatConsumer.as_asgi())
# ]


# import app.routing
from django.urls import re_path,path
from chat.consumers import TextRoomConsumer
websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", TextRoomConsumer.as_asgi()),
    # path('ws/<str:room_name>/', TextRoomConsumer.as_asgi()),

]