from django.db.models import Q
from django.http.response import JsonResponse
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages

import io, csv

from .models import (
    Kantor, Jabatan, Profile, 
    Perusahaan, Tenaga_kerja, User_Profile
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
    # print(request.user.profile_set.values('pk')[0])
    datas = Perusahaan.objects.all()
    return render(request, 'kepesertaan/data_user.html', {'datas':datas})

@csrf_exempt
def Daftar_Perusahaan(request):
    npp = request.POST.get('npp')
    nama_pers = request.POST.get('nama_pemberi_kerja')
    nik = request.POST.get('nik')
    nama = request.POST.get('nama_lengkap')
    # jabatan = request.POST.get('jabatan')
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

    try:
        if password1 == password2 :
            user = User.objects.create(username=username, password=password1)
            user_prof = User_Profile.objects.create(username_id=user.pk, nama=nama, nik=nik,
                email=email, no_hp=no_hp)
            Perusahaan.objects.create(profile_id=user_prof.pk,npp=npp, nama_perusahaan=nama_pers,
                alamat=alamat, desa_kel=desa_kel, kecamatan=kecamatan, kota_kab=kota_kab,
                pembina_id=pembina)

            return JsonResponse({'success':'done'})
        else:
            return JsonResponse({'error':'Password tidak sama!'})
    except:
        return JsonResponse({'error':'Pastikan semua data terisi dan benar!'})

def save_to_models(request):
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Hanya support file csv')
    read_file = csv_file.read().decode('utf-8')
    io_string = io.StringIO(read_file)
    next(io_string)
    for col in csv.reader(io_string, delimiter=',', quotechar="|"):
        print(col[:1])
    return render(request, 'kepesertaan/upload.html')
    