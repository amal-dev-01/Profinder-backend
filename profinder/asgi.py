"""
ASGI config for profinder project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from chat.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'profinder.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http":application,
    "websocket":URLRouter(websocket_urlpatterns)
})
