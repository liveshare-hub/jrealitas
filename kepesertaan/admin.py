from django.contrib import admin

from .models import (Kantor, Jabatan, Profile,
    Perusahaan, Perusahaan_user, Tenaga_kerja)


admin.site.register(Kantor)
admin.site.register(Jabatan)
admin.site.register(Profile)
admin.site.register(Perusahaan_user)
admin.site.register(Perusahaan)
admin.site.register(Tenaga_kerja)