from django.contrib import admin

from .models import (Kantor, Jabatan, Profile,
    Perusahaan, Tenaga_kerja, Informasi, Bidang)


admin.site.register(Kantor)
admin.site.register(Jabatan)
admin.site.register(Profile)
admin.site.register(Bidang)
admin.site.register(Perusahaan)
admin.site.register(Tenaga_kerja)
admin.site.register(Informasi)