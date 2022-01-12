from django.urls import path, include
# from django_private_chat2 import urls as django_private_chat2_urls
from django_private_chat import urls as django_private_chat_urls
from . import views

urlpatterns = [
    path('', include(django_private_chat_urls)),
    # path('<str:room_name>/', views.room, name='room'),
]
