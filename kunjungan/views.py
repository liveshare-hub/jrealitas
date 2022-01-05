from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from kepesertaan.models import Profile
from .models import berita_kunjungan

from .form import KunjunganForm

@login_required(login_url='/accounts/login/')
def kunjungan(request):
    user = request.user
    profile = Profile.objects.select_related('username').get(username__username=user)
    
    # print(profile.pk)
    if profile:
        data_kunjungan = berita_kunjungan.objects.select_related('petugas').filter(petugas__username__username=profile.username)
        # data_kunjungan = berita_kunjungan.objects.select_related('petugas').all()
    else:
        data_kunjungan = berita_kunjungan.objects.none

    if request.method == 'POST':
        forms = KunjunganForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('kunjungan-list')
    else:
        forms = KunjunganForm()
    context = {
        'datas':data_kunjungan,
        'profile':profile,
        'form':forms,
    }

    return render(request, 'kunjungan/index.html',context)

@login_required(login_url='/accounts/login/')
@csrf_exempt
def simpan_kunjungan(request):
    petugas = request.POST['petugas']
    nama = request.POST['nama']
    jabatan = request.POST['jabatan']
    alamat = request.POST['alamat']
    no_hp = request.POST['no_hp']
    tujuan = request.POST['tujuan']
    hasil = request.POST['hasil']

    profile = Profile.objects.select_related('username').get(username__username=petugas)
    if profile:
        buat_bak = berita_kunjungan.objects.create(petugas_id=profile.pk, to_nama=nama, to_jabatan=jabatan,
            to_alamat=alamat, to_no_hp=no_hp, tujuan=tujuan, hasil=hasil)
        return JsonResponse({'success':'Berita Acara Berhasil di simpan'})
    return JsonResponse({'error':'Gagal Disimpan! Periksa Kembali Data Anda'})


