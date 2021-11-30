"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

django.setup()

from notification.consumers import NotificationConsumer

websockets = URLRouter([path("ws/notification/", NotificationConsumer.as_asgi())])

application = ProtocolTypeRouter(
    {
        # websocket handler
        "websocket": AuthMiddlewareStack(websockets),
    }
)
