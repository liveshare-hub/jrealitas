from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (index, data_user, Daftar_Perusahaan, save_to_models, download_excel,
    informasi, Daftar_Pembina, daftar_perusahaan_admin,download_excel_admin, save_to_models_admin)

urlpatterns = [
    path('', index, name='dashboard'),
    path('user/data/', data_user, name='user_data'),
    path('create/npp/', Daftar_Perusahaan, name='daftar-npp'),
    path('create/pembina/', Daftar_Pembina, name='daftar-pembina'),
    path('create/perusahaan/', daftar_perusahaan_admin, name='daftar-perusahaan'),
    path('templates/upload/', save_to_models, name='upload-npp'),
    path('templates/admin/upload/', save_to_models_admin, name='upload-npp-admin'),
    path('templates/download/', download_excel, name='download-npp'),
    path('templates/admin/download/', download_excel_admin, name='download-npp-admin'),
    path('informasi/', informasi, name='informasi'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
