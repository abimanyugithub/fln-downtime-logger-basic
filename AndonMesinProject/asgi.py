"""
ASGI config for AndonMesinProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from AndonMesinApp import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AndonMesinProject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Menangani HTTP
    "websocket": AuthMiddlewareStack(  # Menangani WebSocket
        URLRouter([
            path('ws/some_path/', consumers.MyWebSocketConsumer.as_asgi()),  # Routing URL WebSocket
        ])
    ),
})
