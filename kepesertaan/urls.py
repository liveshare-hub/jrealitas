from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (index, data_user, Daftar_Perusahaan, save_to_models, download_excel,
    informasi, Daftar_Pembina, buat_info, create_info_user, page_tk, list_tk_npp, download_tk_excel,
    save_tk_to_models, edit_profile,update_binaan, edit_profile_perusahaan, pindah_binaan)

urlpatterns = [
    path('', index, name='dashboard'),
    path('user/data/', data_user, name='user_data'),
    path('edit/user/<int:pk>/', edit_profile, name='edit-profile'),
    path('create/npp/', Daftar_Perusahaan, name='daftar-npp'),
    path('update/perusahaan/', edit_profile_perusahaan, name='edit-npp'),
    path('create/pembina/', Daftar_Pembina, name='daftar-pembina'),
    path('update/binaan/', update_binaan, name='update-binaan'),
    path('pindah/binaan/', pindah_binaan, name='pindah-binaan'),
    path('templates/upload/', save_to_models, name='upload-npp'),
    path('templates/download/', download_excel, name='download-npp'),
    path('templates/tk/download/', download_tk_excel, name='download-tk-excel'),
    path('templates/tk/upload/', save_tk_to_models, name='upload-tk'),
    path('page/perusahaan/', page_tk, name='page-tk'),
    path('informasi/<str:npp>/list/tk/', list_tk_npp, name='list-tk'),
    path('informasi/create', buat_info, name='buat-info'),
    path('informasi/create/user/ajax', create_info_user, name='create-info-user'),
    path('informasi/', informasi, name='informasi'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
