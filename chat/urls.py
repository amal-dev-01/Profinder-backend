from django.urls import path,include
from chat.views import  ListUser,MessageListView,MessageDetailView
from chat.routing import websocket_urlpatterns





urlpatterns = [
    path("chat/", ListUser.as_view(), name="chat"),
    # path("chat/", MessageList.as_view(), name="chat"),
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('ws/', include(websocket_urlpatterns)),
]


