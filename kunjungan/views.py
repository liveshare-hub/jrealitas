from django.shortcuts import redirect, render

from kepesertaan.models import Profile
from .models import berita_kunjungan

from .form import KunjunganForm


def kunjungan(request):
    user = request.user
    profile = Profile.objects.select_related('username').get(username__username=user)
    print(profile.username)
    # print(profile.pk)
    if profile:
        data_kunjungan = berita_kunjungan.objects.select_related('petugas').filter(petugas__username__username=profile.username)
        # data_kunjungan = berita_kunjungan.objects.select_related('petugas').all()
    else:
        data_kunjungan = berita_kunjungan.objects.none
    context = {
        'datas':data_kunjungan,
        'profile':profile,
    }

    return render(request, 'kunjungan/index.html',context)

def buat_kunjungan(request):
    if request.method == 'POST':
        forms = KunjunganForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('kunjungan-list')
    else:
        forms = KunjunganForm()
    return render(request, 'kunjungan/buat_kunjungan.html',{'form':forms})
