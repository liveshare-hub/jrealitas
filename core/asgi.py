"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
# import sys

# sys.path.insert(0, "/home/reah4319/jrealitas/core")


import os

from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.urls import path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 routing.websocket_urlpatterns
#             )
#         )
#     )
# })


# django_asgi_app = get_asgi_application()
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

# from chat.consumers import ChatConsumer

# application = ProtocolTypeRouter({
#     'websocket':AuthMiddlewareStack(
#         URLRouter([
#             path('ws/<int:id>', ChatConsumer)
#         ])
#     )
# })
