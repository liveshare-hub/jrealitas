from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
    datas = Perusahaan.objects.all()
    return render(request, 'kepesertaan/data_user.html', {'datas':datas})