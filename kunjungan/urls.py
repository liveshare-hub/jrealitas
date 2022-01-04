from django.urls import path
from . import views

urlpatterns = [
    path('', views.kunjungan, name='kunjungan-list'),
    path('buat/', views.buat_kunjungan, name='buat-kunjungan')
]
