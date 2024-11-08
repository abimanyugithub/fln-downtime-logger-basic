"""
ASGI config for AndonMesinProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AndonMesinProject.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from AndonMesinApp import consumers, routing
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

application = get_asgi_application()

'''
ws_patterns= [
    path('ws/mesin/',consumers.MesinConsumer.as_asgi())
]
'''

application= ProtocolTypeRouter(
    {
        'http': application,
        'websocket': AllowedHostsOriginValidator(
            # AuthMiddlewareStack(URLRouter(ws_patterns))
            AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
        )
    }
)