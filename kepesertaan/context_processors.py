from kunjungan.models import berita_kunjungan
from .models import Informasi, Profile, Perusahaan, Tenaga_kerja
from django.db.models import Q, Sum
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
# from .models import Profile

def info_context(request):
    # print(request.user)
    

    # jabatan = request.user.profile_set.values('jabatan__kode_jabatan')
    # pejabat = Profile.objects.select_related('username','jabatan').filter(Q(jabatan__pk=1) | Q(jabatan__pk=2) | Q(jabatan__pk=3),username__username=request.user)
    if request.user.is_authenticated or request.user.is_superuser:
        pejabat = Profile.objects.select_related('username','jabatan').all()
        # admin = User.objects.filter(username=request.user,groups__name__in=['admin',])
        admin = User.objects.filter(username=request.user,is_superuser=True)
        
        kepala = pejabat.filter(Q(jabatan__kode_jabatan=70) | Q(jabatan__kode_jabatan=701),username__username=request.user)
        pembina = pejabat.filter(Q(jabatan__kode_jabatan=7) | Q(jabatan__kode_jabatan=8), username__username=request.user)
        seluruh_pembina = pejabat.filter(Q(jabatan__kode_jabatan=7) | Q(jabatan__kode_jabatan=8)).exclude(username__username=request.user)
        pelayanan = pejabat.filter(Q(jabatan__kode_jabatan=3) | Q(jabatan__kode_jabatan=4), username__username=request.user)
        # pejabat = Profile.objects.select_related('username','jabatan').filter(jabatan__kode_jabatan=jabatan[0]['jabatan__kode_jabatan'],username__username=request.user)
        if admin.exists():
            total_npp = Perusahaan.objects.all().count()
            infos = Informasi.objects.all().order_by('-created')[:5]
            total_tk = Tenaga_kerja.objects.all().count()
            total_kunjungan = berita_kunjungan.objects.all().count()
            context = {
                'admin':admin,'total_tk':total_tk,'total_npp':total_npp,'total_kunjungan':total_kunjungan,
                'info':infos
            }
            return context

        elif pembina.exists():
            infos = Informasi.objects.select_related('created_by').filter(created_by__username=request.user).order_by('-created')[:5]
            total_npp = Perusahaan.objects.select_related('pembina').filter(pembina__username__username=request.user).count()
            total_kunjungan = berita_kunjungan.objects.select_related('petugas').filter(petugas__username__username=request.user).count()
            total_tk = Tenaga_kerja.objects.select_related('npp').filter(npp__pembina__username__username=request.user).count()

            context = {
                'info':infos, 'pembina':pembina, 'total_npp':total_npp, 'total_tk':total_tk, 'total_kunjungan':total_kunjungan, 'pelayanan':pelayanan,
                'seluruh_pembina':seluruh_pembina
            }
            return context
        else:
            infos = Informasi.objects.select_related('user').filter(user__username=request.user).order_by('-created')[:5]
            workers = Tenaga_kerja.objects.select_related('npp').filter(npp__npp=request.user)
            total_tk = workers.count()
            perusahaan = Perusahaan.objects.filter(npp=request.user)
            cek_valid = perusahaan.filter(Q(email__isnull=True) | Q(no_hp__isnull=True) | Q(npwp_prsh__isnull=True))
            if perusahaan.exists():
                pic = perusahaan[0].nama_pic
            else:
                pic = None
            counter = 0
            total = 14
            if cek_valid.exists():
                
                if cek_valid[0].email is None:
                    counter +=1
                if cek_valid[0].no_hp is None:
                    counter +=1
                if cek_valid[0].npwp_prsh is None:
                    counter +=1
                if cek_valid[0].nik is None:
                    counter +=1
                if cek_valid[0].alamat is None:
                    counter +=1
                if cek_valid[0].kode_pos is None:
                    counter +=1
                if cek_valid[0].desa_kel is None:
                    counter +=1
                if cek_valid[0].kecamatan is None:
                    counter +=1
                if cek_valid[0].kota_kab is None:
                    counter +=1
                
                
            persen_val = 100 - (100 * float(counter)/float(total))  
            
            kunjungan_pembina = berita_kunjungan.objects.select_related('petugas').filter(to_perusahaan__npp=request.user).count()
            context = {
                'info':infos,
                'total_tk':total_tk,
                'workers':workers,
                'pic':pic,
                'total_kunjungan':kunjungan_pembina,
                'cek_valid':cek_valid,
                'persen_val':persen_val,
            }
            return context
    else:
        return {}
