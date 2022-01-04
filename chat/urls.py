from django.urls import path

from . import views

urlpatterns = [
    path('', views.messages_page, name='chat-index'),
    # path('<str:room_name>/', views.room, name='room'),
]
