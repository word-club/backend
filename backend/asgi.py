"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from notification.consumers import NotificationConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

websockets = URLRouter([path("ws/notification/", NotificationConsumer.as_asgi())])

application = ProtocolTypeRouter(
    {
        # websocket handler
        "websocket": AuthMiddlewareStack(websockets),
    }
)
