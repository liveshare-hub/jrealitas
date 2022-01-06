from django.urls import path
from . import views

urlpatterns = [
    path('', views.kunjungan, name='kunjungan-list'),
    path('buat/', views.simpan_kunjungan, name='buat-kunjungan'),
    path('detil/<int:pk>/', views.detail_kunjungan, name='detil-kunjungan'),

]
