"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()

# django_asgi_app = get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>', ChatConsumer)
        ])
    )
})
