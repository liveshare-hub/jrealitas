from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='admindex'),
    path('create-user/', views.page_user, name='page-user'),
    path('create-user/ajax/', views.create_user_internal, name='create-user-internal')
]
