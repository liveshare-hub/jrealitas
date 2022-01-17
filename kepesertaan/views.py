from django.contrib.auth.hashers import make_password
from django.core.checks.messages import Info
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from datetime import datetime
from cryptography.fernet import Fernet
import pandas as pd
from io import StringIO, BytesIO
import xlsxwriter, json

from .forms import InformasiForm

from .models import (
    Informasi, Kantor, Jabatan, Profile, 
    Perusahaan, Tenaga_kerja
)

fs = FileSystemStorage(location='/informasi/attachment')

@login_required(login_url='/accounts/login/')
def index(request):
    user = request.user
    jabatan = Profile.objects.select_related('username').filter(username__username=user)
    
    if jabatan.filter(Q(jabatan__kode_jabatan=70) | Q(jabatan__kode_jabatan=703) | Q(jabatan__kode_jabatan=701)):
        total = Perusahaan.objects.all()
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
    user = request.user
    profile = Profile.objects.select_related('username').filter(username__username=user)
    kepala = profile.filter(Q(jabatan__kode_jabatan=70) | Q(jabatan__kode_jabatan=701))
    keps = profile.filter(Q(jabatan__kode_jabatan=1) | Q(jabatan__kode_jabatan=2))
    ply = profile.filter(jabatan__kode_jabatan=703)
    if kepala.exists() or ply.exists():
        datas = Perusahaan.objects.all()
        profiles = Profile.objects.select_related('username').filter(Q(jabatan__kode_jabatan=1) | Q(jabatan__kode_jabatan=2))
        context = {
        'datas':datas,
        'profiles':profiles,
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
    if password1 == password2 :
        user = User.objects.create(username=username, password=password1)
        # user_prof = User_Profile.objects.create(username_id=user.pk, nama=nama, nik=nik,
        #     email=email, no_hp=no_hp)
        Profile.objects.create(username_id=user.pk,nama=nama, jabatan_id=jabatan,
            email=email, kode_kantor_id=kd_kantor, no_hp=no_hp)

        return JsonResponse({'success':'done'})
    else:
        return JsonResponse({'error':'Password tidak sama!'})
    # except:
    #     return JsonResponse({'error':'Pastikan semua data terisi dan benar!'})

@login_required(login_url='/accounts/login/')
@csrf_exempt
def Daftar_Perusahaan(request):
    npp = request.POST.get('npp') or request.POST.get('npp_admin')
    nama_pers = request.POST.get('nama_pemberi_kerja') or request.POST.get('nama_pemberi_kerja_admin')
    nik = request.POST.get('nik') or request.POST.get('nik_admin')
    nama = request.POST.get('nama_lengkap') or request.POST.get('nama_lengkap_admin')
    jabatan = request.POST.get('id_jabatan')
    pembina = request.POST.get('pembina_id') or request.POST.get('id_pembina_admin')
    email = request.POST.get('email') or request.POST.get('email_admin')
    no_hp = request.POST.get('no_hp') or request.POST.get('no_hp_admin')
    alamat = request.POST.get('alamat_perusahaan') or request.POST.get('alamat_perusahaan_admin')
    desa_kel = request.POST.get('desa_kel') or request.POST.get('desa_kel_admin')
    kecamatan = request.POST.get('kecamatan') or request.POST.get('kecamatan_admin')
    kota_kab = request.POST.get('kota_kab') or request.POST.get('kota_kab_admin')
    username = request.POST.get('username') or request.POST.get('username_admin')
    password1 = request.POST.get('password1') or request.POST.get('password1_admin')
    password2 = request.POST.get('password2') or request.POST.get('password2_admin')


    if jabatan == 3:
        if password1 == password2 :
            user = User.objects.create(username=username, password=password1)
            # user_prof = User_Profile.objects.create(username_id=user.pk, nama=nama, nik=nik,
            #     email=email, no_hp=no_hp)
            Perusahaan.objects.create(username_id=user.pk,nama=nama, nik=nik, email=email,
                no_hp=no_hp, npp=npp, nama_perusahaan=nama_pers,
                alamat=alamat, desa_kel=desa_kel, kecamatan=kecamatan, kota_kab=kota_kab,
                pembina_id=int(pembina))

            return JsonResponse({'success':'done'})
        else:
            return JsonResponse({'error':'Password tidak sama!'})
    else:
        if password1 == password2 :
            user = User.objects.create(username=username, password=password1)
            
            # user_prof = User_Profile.objects.create(username_id=user.pk, nama=nama, nik=nik,
            #     email=email, no_hp=no_hp)
            Perusahaan.objects.create(username_id=user.pk,nama=nama, nik=nik, email=email,
                no_hp=no_hp, npp=npp, nama_perusahaan=nama_pers,
                alamat=alamat, desa_kel=desa_kel, kecamatan=kecamatan, kota_kab=kota_kab,
                pembina_id=int(pembina))

            return JsonResponse({'success':'done'})
        else:
            return JsonResponse({'error':'Password tidak sama!'})

@login_required(login_url='/accounts/login/')
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
            obj = Perusahaan.objects.select_related('pembina','username').create(nama=dbframe.NAMA_LENGKAP, nik=dbframe.NIK, email=dbframe.EMAIL,
                no_hp=dbframe.NO_HANDPHONE, npp=dbframe.NPP, nama_perusahaan=dbframe.NAMA_PERUSAHAAN, alamat=dbframe.ALAMAT_PERUSAHAAN,
                desa_kel=dbframe.DESA_KELURAHAN, kecamatan=dbframe.KECAMATAN, kota_kab=dbframe.KOTA_KABUPATEN, username_id=user.pk, pembina_id=pembina)
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
    worksheet.write('C1','NAMA_LENGKAP', bold)
    worksheet.write('D1','NIK', bold)
    worksheet.write('E1','JABATAN',bold)
    worksheet.write('F1','EMAIL', bold)
    worksheet.write('G1','NO_HANDPHONE', bold)
    worksheet.write('H1','ALAMAT_PERUSAHAAN', bold)
    worksheet.write('I1','DESA_KELURAHAN', bold)
    worksheet.write('J1','KECAMATAN', bold)
    worksheet.write('K1','KOTA_KABUPATEN', bold)

    row = 1
    col = 0
    try:
        datas = Perusahaan.objects.all()[1]
        # npp = datas[0].npp
        for data in datas:
            worksheet.write(row, col, data.npp)
            worksheet.write(row, col+1, data.nama_perusahaan)
            worksheet.write(row, col+2, data.nama)
            worksheet.write(row, col+3, data.nik)
            worksheet.write(row, col+4, "HRD")
            worksheet.write(row, col+5, data.email)
            worksheet.write(row, col+6, data.no_hp)
            worksheet.write(row, col+7, data.alamat)
            worksheet.write(row, col+8, data.desa_kel)
            worksheet.write(row, col+9, data.kecamatan)
            worksheet.write(row, col+10, data.kota_kab)
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
    
    context = {
        'npps':npp
    }

    return render(request, 'kepesertaan/page_tk.html', context)


@login_required(login_url='/accounts/login/')
def list_tk_npp(request, npp):
    workers = Tenaga_kerja.objects.select_related('npp').filter(npp__npp=npp).all()
    is_npp = Perusahaan.objects.filter(npp=npp)

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

    worksheet.write_string(row, col, npp)
    worksheet.write(row, col+1, "SI POLAN")
    worksheet.write(row, col+2, "21013210001")
    worksheet.write(row, col+3, "01-01-1997")
    worksheet.write(row, col+4, "01-2021")
    worksheet.write(row, col+5, "10-2021")
    worksheet.write(row, col+6, "siplan@mail.com")
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