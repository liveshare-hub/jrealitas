from django.contrib import admin

from .models import (Kantor, Jabatan, Profile, User_Profile,
    Perusahaan, Tenaga_kerja, Informasi)


admin.site.register(Kantor)
admin.site.register(Jabatan)
admin.site.register(Profile)
admin.site.register(User_Profile)
admin.site.register(Perusahaan)
admin.site.register(Tenaga_kerja)
admin.site.register(Informasi)