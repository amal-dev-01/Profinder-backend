from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from chat.routing import websocket_urlpatterns
from chat.views import (ChatHistoryView, DeleteMessageView, ListUser,
                        MessageList)

urlpatterns = [
    path("ws/", include(websocket_urlpatterns)),
    path("chat/", ListUser.as_view(), name="chat"),
    path("messages/", MessageList.as_view()),
    path('messages/<int:message_id>/', MessageList.as_view(), name='message-detail'),
    path(
        "chat_history/<str:room_name>/", ChatHistoryView.as_view(), name="chat_history"
    ),
    path(
        "delete_message/<int:message_id>/",
        DeleteMessageView.as_view(),
        name="delete_message",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
