from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('testing/', views.index, name='index'),
    path('<str:room_name>/', views.chatbox, name='chat'),
    path('create/thread/', views.create_chat, name='create-thread'),
    path('save/chat/', views.save_chat, name='save-chat'),
    path('load/chat/', views.load_chat),
    path('read/done/', views.is_read_chat),
    path('load/read/', views.load_read)
]
