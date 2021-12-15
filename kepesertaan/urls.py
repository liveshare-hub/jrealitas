from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (index, data_user, Daftar_Perusahaan, save_to_models, download_excel,
    informasi)

urlpatterns = [
    path('', index, name='dashboard'),
    path('user/data/', data_user, name='user_data'),
    path('create/npp/', Daftar_Perusahaan, name='daftar-npp'),
    path('templates/upload/', save_to_models, name='upload-npp'),
    path('templates/download/', download_excel, name='download-npp'),
    path('informasi/', informasi, name='informasi'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
