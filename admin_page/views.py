from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.db.models import Q, Count

from kepesertaan.models import Kantor, Bidang, Jabatan, Perusahaan, Profile, Tenaga_kerja
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from core.decorators import adminuser_only

from .forms import BidangForm, JabatanForm, PembinaForm



@login_required
@adminuser_only
def index(request):
    # data = []
    profile = Profile.objects.select_related('username','jabatan').all()
    per_profile = profile.filter(Q(jabatan__kode_jabatan=7) | Q(jabatan__kode_jabatan=8))

    data = per_profile.annotate(num_npp=Count('perusahaan', distinct=True)).annotate(total_tk=Count('perusahaan__tenaga_kerja'))

    # for d in data:
    #     print(d.username.username," : ", d.num_npp, " : ", d.total_tk)
    context = {
        'datas':data
    }
    return render(request, 'admin_page/index.html', context)

@login_required
@adminuser_only
def page_user(request):
    datas = Profile.objects.all()
    form = PembinaForm(request.POST)
    return render(request, 'admin_page/buat_profile.html',{'form':form, 'datas':datas})

@login_required
def create_bidang(request):
    form = BidangForm()
    if request.method == 'POST':
        form = BidangForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('admindex')
    return render(request, 'admin_page/buat_bidang.html', {'form':form})

@login_required
@adminuser_only
def create_user_internal(request):
    kd_kantor = request.POST.get('kd_kantor')
    nama = request.POST.get('nama')
    jabatan = request.POST.get('jabatan')
    email = str(request.POST.get('email')).lower()
    no_hp = request.POST.get('no_hp')
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')


    cek_user = User.objects.filter(username=username)
    if cek_user.exists():
        return JsonResponse({'error':'User sudah pernah terdaftar!'})
    else:
        if password1 == password2 :
            group = Group.objects.get(name='pembina')
            password = make_password(password1, hasher='default')
            user = User.objects.create(username=username, password=password, email=email)
            user.groups.add(group.id)
            user.save()

            Profile.objects.create(username_id=user.pk,nama=nama, jabatan_id=jabatan,
                kode_kantor_id=kd_kantor, no_hp=no_hp)

            return JsonResponse({'success':'done'})
        else:
            return JsonResponse({'data_error':'Password tidak sama!'})
            
            
