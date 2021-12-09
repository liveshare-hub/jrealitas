from django.urls import path

from .views import index, data_user

urlpatterns = [
    path('', index, name='dashboard'),
    path('user/data/', data_user, name='user_data')
]
