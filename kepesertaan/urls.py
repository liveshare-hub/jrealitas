from django.urls import path

from .views import index, data_user, Daftar_Perusahaan, save_to_models

urlpatterns = [
    path('', index, name='dashboard'),
    path('user/data/', data_user, name='user_data'),
    path('create/npp/', Daftar_Perusahaan, name='daftar-npp'),
    path('upload/perusahaan/', save_to_models, name='upload-npp'),
]
