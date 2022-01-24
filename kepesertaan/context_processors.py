from kunjungan.models import berita_kunjungan
from .models import Informasi, Profile, Perusahaan, Tenaga_kerja
from django.db.models import Q, Sum
from django.shortcuts import redirect
# from .models import Profile

def info_context(request):
    # print(request.user)
    

    # jabatan = request.user.profile_set.values('jabatan__kode_jabatan')
    # pejabat = Profile.objects.select_related('username','jabatan').filter(Q(jabatan__pk=1) | Q(jabatan__pk=2) | Q(jabatan__pk=3),username__username=request.user)
    if request.user.is_authenticated:
        pejabat = Profile.objects.select_related('username','jabatan').all()
        kepala = pejabat.filter(Q(jabatan__kode_jabatan=70) | Q(jabatan__kode_jabatan=701),username__username=request.user)
        pembina = pejabat.filter(Q(jabatan__kode_jabatan=7) | Q(jabatan__kode_jabatan=8), username__username=request.user)
        # pejabat = Profile.objects.select_related('username','jabatan').filter(jabatan__kode_jabatan=jabatan[0]['jabatan__kode_jabatan'],username__username=request.user)
        if kepala.exists() or request.user.is_superuser:
            infos = Informasi.objects.all().order_by('-created')[:5]
            total_npp = Perusahaan.objects.all().count()
            total_tk = Tenaga_kerja.objects.all().count()
            total_kunjungan = berita_kunjungan.objects.all().count()
            # profile = Profile.objects.select_related('username','jabatan').filter(jabatan__kode_jabatan=jabatan[0]['jabatan__kode_jabatan'])
            context = {
                'info':infos, 'kepala':kepala, 'total_npp':total_npp, 'total_tk':total_tk,
                'total_kunjungan':total_kunjungan
            }
            return context
        elif pembina.exists():
            infos = Informasi.objects.select_related('created_by').filter(created_by__username=request.user).order_by('-created')[:5]
            total_npp = Perusahaan.objects.select_related('pembina').filter(pembina__username__username=request.user).count()
            total_kunjungan = berita_kunjungan.objects.select_related('petugas').filter(petugas__username__username=request.user).count()
            total_tk = Tenaga_kerja.objects.select_related('npp').filter(npp__pembina__username__username=request.user).count()

            context = {
                'info':infos, 'pembina':pembina, 'total_npp':total_npp, 'total_tk':total_tk, 'total_kunjungan':total_kunjungan
            }
            return context
        else:
            infos = Informasi.objects.select_related('user').filter(user__username=request.user).order_by('-created')[:5]
            total_tk = Tenaga_kerja.objects.select_related('npp').filter(npp__npp=request.user).count()
            perusahaan = Perusahaan.objects.filter(npp=request.user)
            if perusahaan.exists():
                pic = perusahaan[0].nama_pic
            else:
                pic = None
            kunjungan_pembina = berita_kunjungan.objects.select_related('petugas').filter(to_perusahaan__npp=request.user).count()
            context = {
                'info':infos,
                'total_tk':total_tk,
                'pic':pic,
                'total_kunjungan':kunjungan_pembina
            }
            return context
    else:
        return {}
