from kunjungan.models import berita_kunjungan
from .models import Informasi, Profile, Perusahaan, Tenaga_kerja
from django.db.models import Q, Sum
# from .models import Profile

def info_context(request):
    # print(request.user)
    
    try:
        # jabatan = request.user.profile_set.values('jabatan__kode_jabatan')
        print(request.user.is_authenticated)
        pejabat = Profile.objects.select_related('username','jabatan').filter(Q(jabatan__pk=1) | Q(jabatan__pk=2) | Q(jabatan__pk=3),username__username=request.user)
        # pejabat = Profile.objects.select_related('username','jabatan').filter(jabatan__kode_jabatan=jabatan[0]['jabatan__kode_jabatan'],username__username=request.user)
        if pejabat.exists():
            datas = Informasi.objects.all().order_by('-created')[:5]
            total_npp = Perusahaan.objects.all().count()
            total_tk = Tenaga_kerja.objects.all().count()
            kunjungan = berita_kunjungan.objects.all().count()
            # profile = Profile.objects.select_related('username','jabatan').filter(jabatan__kode_jabatan=jabatan[0]['jabatan__kode_jabatan'])
            context = {
                'info':datas, 'kepala':pejabat, 'total_npp':total_npp, 'total_tk':total_tk,
                'total_kunjungan':kunjungan
            }
            return context
        else:
            datas = Informasi.objects.select_related('user').filter(user__username=request.user).order_by('-created')[:5]
            return {'info':datas, 'kepala':pejabat}
    except:
        pass