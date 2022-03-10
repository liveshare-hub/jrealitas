from calendar import c
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from django.core.files.storage import FileSystemStorage

from datetime import datetime
from cryptography.fernet import Fernet
import pandas as pd
from io import BytesIO
import xlsxwriter, json


from .models import (
    Informasi, Kantor, Jabatan, Profile, 
    Perusahaan, Tenaga_kerja
)

from .forms import PembinaForm, PerusahaanForm

fs = FileSystemStorage(location='/informasi/attachment')

@login_required(login_url='/accounts/login/')
def index(request):
    user = request.user
    jabatan = Profile.objects.select_related('username').filter(username__username=user)
    
    if jabatan.filter(Q(jabatan__kode_jabatan=70) | Q(jabatan__kode_jabatan=703) | Q(jabatan__kode_jabatan=701)):
        total = Perusahaan.objects.all()
    elif jabatan.filter(Q(jabatan__kode_jabatan=1) | Q(jabatan__kode_jabatan=2)):
        total = Perusahaan.total_npp(kwargs=user.username)
        
    else:
        total = 0
   
    #dashboard
    return render(request, 'kepesertaan/dashboard.html')


# def edit_perusahaan(request):


@login_required(login_url='/accounts/login/')
def data_user(request):
    user = request.user
    profile = Profile.objects.select_related('username').filter(username__username=user)
    kepala = profile.filter(Q(jabatan__kode_jabatan=70) | Q(jabatan__kode_jabatan=701))
    keps = profile.filter(Q(jabatan__kode_jabatan=7) | Q(jabatan__kode_jabatan=8))
    ply = profile.filter(jabatan__kode_jabatan=703)
    if kepala.exists() or ply.exists():
        datas = Perusahaan.objects.all()
        # profiles = Profile.objects.select_related('username').filter(Q(jabatan__kode_jabatan=7) | Q(jabatan__kode_jabatan=8))

        context = {
        'datas':datas,
        'profiles':keps,
        'kepala':kepala,
        'keps':keps,
        'ply':ply,
    }
    elif keps.exists():
        datas = Perusahaan.objects.select_related('username','pembina').filter(pembina__username__username=user)
        context = {
        'datas':datas,
        'kepala':kepala,
        'keps':keps,
        'ply':ply,
    }
    else:
        tk_npp = Tenaga_kerja.objects.select_related('npp').filter(npp__npp=request.user)

        context = {
            'workers':tk_npp
        }
    return render(request, 'kepesertaan/data_user.html', context)

@login_required
def edit_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    bidang_id = Profile.objects.filter(pk=pk)
    if request.method == 'POST':
        form = PembinaForm(request.POST, instance=profile, bidang_id=bidang_id[0].jabatan.bidang.kode_bidang)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PembinaForm(instance=profile, bidang_id=bidang_id[0].jabatan.bidang.kode_bidang)
        return render(request, 'kepesertaan/edit_profile.html', {'form':form})

@login_required
def update_binaan(request):
    npp = request.POST.get('npp')
    pembina = request.POST.get('pembina')
    # print(pembina)
    q = Perusahaan.objects.select_related('username','pembina').get(npp=npp)
    q.pembina_id = int(pembina)
    q.save()
    # print(q.pembina.username.pk)

    return JsonResponse({'msg':'Berhasil'})

@login_required
def pindah_binaan(request):
    datas = Perusahaan.objects.select_related('pembina').filter(pembina__username__username=request.user)
    
    context = {
        'datas':datas
    }
    return render(request, 'kepesertaan/pindah_binaan.html',context)


@login_required(login_url='/accounts/login/')
@csrf_exempt
def Daftar_Pembina(request):
    kd_kantor = request.user.profile_set.values('kode_kantor__pk')[0]['kode_kantor__pk']
    
    nama = request.POST.get('nama_pembina')
    jabatan = request.POST.get('jabatan')
    # bidang = request.POST.get('bidang')
    # kepala = request.POST.get('kepala_id')
    email = request.POST.get('email_pembina')
    no_hp = request.POST.get('no_hp_pembina')
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    # try:
    cek_user = User.objects.filter(username=username)
    if cek_user.exists():
        return JsonResponse({'error':'User sudah pernah terdaftar!'})
    else:
        if password1 == password2 :
            user = User.objects.create(username=username, password=password1, email=email)
            # user_prof = User_Profile.objects.create(username_id=user.pk, nama=nama, nik=nik,
            #     email=email, no_hp=no_hp)
            Profile.objects.create(username_id=user.pk,nama=nama, jabatan_id=jabatan,
                kode_kantor_id=kd_kantor, no_hp=no_hp)

            return JsonResponse({'success':'done'})
        else:
            return JsonResponse({'data_error':'Password tidak sama!'})
    # except:
    #     return JsonResponse({'error':'Pastikan semua data terisi dan benar!'})

@login_required(login_url='/accounts/login/')
@csrf_exempt
def Daftar_Perusahaan(request):
    npp = request.POST.get('npp') or request.POST.get('npp_admin')
    nama_pers = request.POST.get('nama_pemberi_kerja') or request.POST.get('nama_pemberi_kerja_admin')
    # nik = request.POST.get('nik') or request.POST.get('nik_admin')
    nama_pic = request.POST.get('nama_lengkap') or request.POST.get('nama_lengkap_admin')
    # jabatan = request.POST.get('id_jabatan')
    pembina = request.POST.get('pembina_id') or request.POST.get('id_pembina_admin')
    # email = request.POST.get('email') or request.POST.get('email_admin')
    # no_hp = request.POST.get('no_hp') or request.POST.get('no_hp_admin')
    # pemilik = request.POST.get('nama_pemilik') or request.POST.get('nama_pemilik_admin')
    # npwp = request.POST.get('npwp') or request.POST.get('npwp_admin')
    # alamat = request.POST.get('alamat_perusahaan') or request.POST.get('alamat_perusahaan_admin')
    # desa_kel = request.POST.get('desa_kel') or request.POST.get('desa_kel_admin')
    # kecamatan = request.POST.get('kecamatan') or request.POST.get('kecamatan_admin')
    # kota_kab = request.POST.get('kota_kab') or request.POST.get('kota_kab_admin')
    # kode_pos = request.POST.get('kode_pos') or request.POST.get('kode_pos_admin')
    username = request.POST.get('username') or request.POST.get('username_admin')
    # password1 = request.POST.get('password1') or request.POST.get('password1_admin')
    # password2 = request.POST.get('password2') or request.POST.get('password2_admin')
    key = Fernet.generate_key()
    fernet = Fernet(key)

    cek_npp = Perusahaan.objects.filter(username__username=username)

    
    if cek_npp.exists():
        return JsonResponse({'error':'Perusahaan sudah pernah terdaftar!'})
    else:
        # if password1 == password2 :
        encsalt = fernet.encrypt(npp.encode())
        salts = encsalt[1:10]
        password = make_password("WELCOME1", salt=[salts.decode('utf-8')])
        user = User.objects.create(username=username, password=password)

        Perusahaan.objects.create(username_id=user.pk,nama_pic=nama_pic, npp=npp,
            nama_perusahaan=nama_pers, pembina_id=int(pembina))

        return JsonResponse({'success':'done'})
        # else:
        #     return JsonResponse({'error':'Password tidak sama!'})
    # else:
    #     if cek_npp.exists():
    #         return JsonResponse({'error':'Perusahaan sudah pernah terdaftar!'})
    #     else:
    #         if password1 == password2 :
    #             encsalt = fernet.encrypt(npp.encode())
    #             password = make_password(password1, salt=[encsalt.decode('utf-8')])
    #             user = User.objects.create(username=username, password=password)
                
    #             Perusahaan.objects.create(username_id=user.pk,nama_pic=nama_pic, nik=nik, email=email,
    #                 no_hp=no_hp, npp=npp, nama_perusahaan=nama_pers, nama_pemilik=pemilik, npwp_prsh=npwp,
    #                 alamat=alamat, desa_kel=desa_kel, kecamatan=kecamatan, kota_kab=kota_kab, kode_pos=kode_pos,
    #                 pembina_id=int(pembina))

    #             return JsonResponse({'success':'done'})
    #         else:
    #             return JsonResponse({'error':'Password tidak sama!'})

def edit_profile_perusahaan(request):
    username = request.user
    cek_npp = Perusahaan.objects.get(npp=username)
    # cek_npp = get_object_or_404(pk=username)
    
    if request.method == 'POST':
        form = PerusahaanForm(request.POST, instance=cek_npp)
        nama_pemilik = request.POST.get('nama_pemilik')
        nik = request.POST.get('nik')
        email = request.POST.get('email')
        no_hp = request.POST.get('no_hp')
        alamat = request.POST.get('alamat')
        kode_pos = request.POST.get('kode_pos')
        npwp_prsh = request.POST.get('npwp_prsh')
        desa_kel = request.POST.get('desa_kel')
        kecamatan = request.POST.get('kecamatan')
        kota_kab = request.POST.get('kota_kab')
        User.objects.filter(username=username).update(email=email)
        Perusahaan.objects.filter(username__username=username).update(nama_pemilik=nama_pemilik,
            nik=nik, email=email, no_hp=no_hp,alamat=alamat,kode_pos=kode_pos,npwp_prsh=npwp_prsh,desa_kel=desa_kel,
            kecamatan=kecamatan,kota_kab=kota_kab)
        return redirect('dashboard')

    #     if form.is_valid():
    #         form.save()
    #         return redirect('dashboard')
    else:
        form = PerusahaanForm(instance=cek_npp)
        return render(request, 'kepesertaan/edit_pers.html', {'form':form})
    

@login_required(login_url='/accounts/login/')
@csrf_exempt
def save_to_models(request):
    pembina = request.user.profile_set.values('pk')[0]['pk']
    
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        
        exceldata = pd.read_excel(myfile)
        
        dbframe = exceldata
        for dbframe in dbframe.itertuples():
            key = Fernet.generate_key()
            fernet = Fernet(key)
            encsalt = fernet.encrypt(dbframe.NPP.encode())
            
            password = make_password(dbframe.NPP, salt=[encsalt.decode('utf-8')])
            user = User.objects.create(username=dbframe.NPP, password=password)
            obj = Perusahaan.objects.select_related('pembina','username').create(nama_pemilik=dbframe.NAMA_PEMILIK_PERUSAHAAN, nik=dbframe.NIK, email=dbframe.EMAIL,
                no_hp=dbframe.NO_HANDPHONE, npp=dbframe.NPP, nama_pic=dbframe.NAMA_PIC, nama_perusahaan=dbframe.NAMA_PERUSAHAAN, alamat=dbframe.ALAMAT_PERUSAHAAN,
                npwp_prsh=dbframe.NPWP_PERUSAHAAN, kode_pos=dbframe.KODE_POS, desa_kel=dbframe.DESA_KELURAHAN, kecamatan=dbframe.KECAMATAN,
                kota_kab=dbframe.KOTA_KABUPATEN, username_id=user.pk, pembina_id=pembina)
            obj.save()

        return JsonResponse({'success':'Done'})
        # return render(request, 'kepesertaan/upload.html',{'upload_url':uploaded_url})
 
    # return render(request, 'kepesertaan/upload.html')

@login_required(login_url='/accounts/login/')
def download_excel(request):
    
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    bold = workbook.add_format({'bold':True})
    worksheet = workbook.add_worksheet()
    worksheet.write('A1','NPP',bold)
    worksheet.write('B1','NAMA_PERUSAHAAN', bold)
    worksheet.write('C1','NAMA_PIC', bold)
    worksheet.write('D1','NIK', bold)
    worksheet.write('E1','JABATAN',bold)
    worksheet.write('F1','EMAIL', bold)
    worksheet.write('G1','NO_HANDPHONE', bold)
    worksheet.write('H1', 'NAMA_PEMILIK_PERUSAHAAN', bold)
    worksheet.write('I1', 'NPWP_PERUSAHAAN', bold)
    worksheet.write('J1','ALAMAT_PERUSAHAAN', bold)
    worksheet.write('K1','DESA_KELURAHAN', bold)
    worksheet.write('L1','KECAMATAN', bold)
    worksheet.write('M1','KOTA_KABUPATEN', bold)
    worksheet.write('N1','KODE_POS', bold)

    row = 1
    col = 0
    try:
        data = Perusahaan.objects.all()[0]
        # npp = datas[0].npp
        # for data in datas:
        #     print(data.npp)
        worksheet.write(row, col, data.npp)
        worksheet.write(row, col+1, data.nama_perusahaan)
        worksheet.write(row, col+2, data.nama_pic)
        worksheet.write(row, col+3, data.nik)
        worksheet.write(row, col+4, "HRD")
        worksheet.write(row, col+5, data.email)
        worksheet.write(row, col+6, data.no_hp)
        worksheet.write(row, col+7, data.nama_pemilik)
        worksheet.write(row, col+8, data.npwp_prsh)
        worksheet.write(row, col+9, data.alamat)
        worksheet.write(row, col+10, data.desa_kel)
        worksheet.write(row, col+11, data.kecamatan)
        worksheet.write(row, col+12, data.kota_kab)
        worksheet.write(row, col+13, data.kode_pos)
    except:
        pass
        
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="uploaded.xlsx"'

    response.write(output.getvalue())
    return response

@login_required(login_url='/accounts/login')
@csrf_exempt
def buat_info(request):
    kepala = Profile.objects.select_related('username').filter(username__username=request.user)
    factories = Perusahaan.objects.all()
    # infos = Informasi.objects.all()
    # form = InformasiForm()
    
    context = {
        # 'form':form,
        'kepala':kepala,
        # 'infos':infos,
        'datas':factories
    }
    return render(request, 'kepesertaan/create_informasi.html',context)

@login_required(login_url='/accounts/login/')
def create_info_user(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        
        isi = request.POST.get('isi')
        attach = request.FILES['attach']
        file1 = fs.save(attach.name, attach)
        attach_url = fs.url(file1)
        
        users = json.loads(request.POST.get('user'))
        
        if users:
            for user in users:
            
                user_id = User.objects.get(pk=user['value'])
                profile_id = Profile.objects.get(username__username=request.user)
                created = Informasi.objects.select_related('user').create(judul=judul, isi=isi, attachment=attach_url, user_id=user_id.id, created_by_id=profile_id.id)
            if created:
                return JsonResponse({'success':'Berhasil'})
            else:
                return JsonResponse({'errors':'Data Gagal Disimpan!'})
        else:
            factories = Perusahaan.objects.all()
            for npp in factories:
                profile_id = Profile.objects.get(username__username=request.user)
                created = Informasi.objects.select_related('user').create(judul=judul, isi=isi, attachment=attach_url, user_id=npp.username.id, created_by_id=profile_id.id)
            if created:
                return JsonResponse({'success':'Berhasil'})
            else:
                return JsonResponse({'errors':'Data Gagal Disimpan'})
                

@login_required(login_url='/accounts/login/')
@csrf_exempt
def informasi(request):

    return render(request, 'kepesertaan/informasi.html')



@login_required(login_url='/accounts/login/')
@csrf_exempt
def page_tk(request):
    user = request.user
    npp = Perusahaan.objects.select_related('username','pembina').filter(pembina__username__username=user)
    workers = Tenaga_kerja.objects.select_related('npp').filter(npp__npp=request.user)
    
    context = {
        'npps':npp
    }

    return render(request, 'kepesertaan/page_tk.html', context)


@login_required(login_url='/accounts/login/')
def list_tk_npp(request, npp):
    workers = Tenaga_kerja.objects.select_related('npp').filter(npp__npp=npp).all()
    is_npp = Perusahaan.objects.filter(npp=npp)[0]

    context = {
        'workers':workers,
        'is_npp':is_npp
    }

    return render(request, 'kepesertaan/list_tk.html', context)


@login_required(login_url='/accounts/login/')
def download_tk_excel(request):
    npp = request.user.username
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    bold = workbook.add_format({'bold':True})
    worksheet = workbook.add_worksheet()
    worksheet.write('A1','NPP',bold)
    worksheet.write('B1','NAMA_LENGKAP', bold)
    worksheet.write('C1','NO_KPJ', bold)
    worksheet.write('D1','TGL_LAHIR',bold)
    worksheet.write('E1','TGL_KEPS', bold)
    worksheet.write('F1','TGL_NA', bold)
    worksheet.write('G1','EMAIL', bold)
    worksheet.write('H1','NO_HANDPHONE', bold)
    

    row = 1
    col = 0

    worksheet.write_string(row, col, "BB04xxxxx")
    worksheet.write(row, col+1, "SI POLAN")
    worksheet.write_string(row, col+2, "21013210001")
    worksheet.write_string(row, col+3, "01-01-1997")
    worksheet.write_string(row, col+4, "01-2021")
    worksheet.write_string(row, col+5, "10-2021")
    worksheet.write_string(row, col+6, "siplan@mail.com")
    worksheet.write_string(row, col+7, "082121234561")
        
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="upload_tk.xlsx"'

    response.write(output.getvalue())
    return response

@login_required(login_url='/accounts/login/')
def save_tk_to_models(request):
    
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        
        exceldata = pd.read_excel(myfile)
        
        dbframe = exceldata
        na = dbframe.TGL_NA
        print(dbframe.NO_KPJ)
        for dbframe in dbframe.itertuples():
            tgl_lhr = datetime.strptime(dbframe.TGL_LAHIR, '%d-%m-%Y')
            tgl_keps = datetime.strptime(dbframe.TGL_KEPS, '%m-%Y')
            no_hp = '0'+str(dbframe.NO_HANDPHONE)
            if (len(na.value_counts())) > 0:
                tgl_na = datetime.strptime(dbframe.TGL_NA, '%m-%Y')
            else:
                tgl_na = None
            npp = Perusahaan.objects.get(npp=dbframe.NPP)
            if npp:

                obj = Tenaga_kerja.objects.select_related('npp').create(npp_id=npp.pk, nama=dbframe.NAMA_LENGKAP, no_kartu=str(dbframe.NO_KPJ), tgl_lahir=tgl_lhr, tgl_keps=tgl_keps,
                    tgl_na=tgl_na, email=dbframe.EMAIL, no_hp=no_hp)
            else:
                return JsonResponse({'Error':'Cek File anda kembali'})
        return JsonResponse({'success':'Done'})