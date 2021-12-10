from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import (
    Kantor, Jabatan, Profile, 
    Perusahaan, Perusahaan_user, Tenaga_kerja
)

@login_required(login_url='/accounts/login/')
def index(request):
    user = request.user
    jabatan = Profile.objects.select_related('username').filter(username__username=user)
    
    if jabatan.filter(Q(jabatan__kode_jabatan=70) | Q(jabatan__kode_jabatan=32) | Q(jabatan__kode_jabatan=703)):
        total = Perusahaan.all()
        print(total)
    elif jabatan.filter(Q(jabatan__kode_jabatan=1) | Q(jabatan__kode_jabatan=2)):
        total = Perusahaan.total_npp(kwargs=user.username)
        print(total)
    else:
        total = 0
   
    #dashboard
    return render(request, 'kepesertaan/dashboard.html')

@login_required(login_url='/accounts/login/')
def data_user(request):
    # print(request.user.profile_set.values('jabatan_id')[0])
    print(request.user.profile_set.values('pk')[0])
    datas = Perusahaan.objects.all()
    return render(request, 'kepesertaan/data_user.html', {'datas':datas})

@csrf_exempt
def Daftar_Perusahaan(request):
    npp = request.POST.get('npp')
    nama_pers = request.POST.get('nama_pemberi_kerja')
    nik = request.POST.get('nik')
    nama = request.POST.get('nama_lengkap')
    jabatan = request.POST.get('jabatan')
    pembina = request.POST.get('pembina_id')
    email = request.POST.get('email')
    no_hp = request.POST.get('no_hp')
    alamat = request.POST.get('alamat_perusahaan')
    desa_kel = request.POST.get('desa_kel')
    kecamatan = request.POST.get('kecamatan')
    kota_kab = request.POST.get('kota_kab')
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if password1 == password2 :
        try:
            User.objects.create(username=username, password=password1)
        except User.DoesNotExist:
            return False

        return JsonResponse({'success':'done'})
    else:
        return JsonResponse({'error':'Password tidak sama!'})