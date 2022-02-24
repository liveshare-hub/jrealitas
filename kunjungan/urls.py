from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.kunjungan, name='kunjungan-list'),
    path('buat/', views.simpan_kunjungan, name='buat-kunjungan'),
    path('detil/<int:pk>/', views.detail_kunjungan, name='detil-kunjungan'),
    # path('detil/<int:pk>/', views.docPDF, name='detil-kunjungan'),
    path('approval/list/', views.daftar_approval_kunjungan, name='list-approval'),
    path('approval/<int:pk>/done/', views.approval_kunjungan, name='approval-kunjungan'),
    path('pdf/<int:pk>/', views.GeneratePDF.as_view(), name='generate-pdf'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
