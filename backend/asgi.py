"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from backend.SocketAuthMiddleware import UserAuthMiddleware

from account.consumers import LoginConsumer
from notification.consumers import NotificationConsumer


websockets = URLRouter(
    [
        path("ws/login/", LoginConsumer.as_asgi()),
        path("ws/notification/", NotificationConsumer.as_asgi()),
    ]
)

application = ProtocolTypeRouter(
    {
         "http": get_asgi_application(),
        # websocket handler
        "websocket": AllowedHostsOriginValidator(UserAuthMiddleware(websockets)),
    }
)
