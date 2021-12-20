from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

import pandas as pd
from io import StringIO, BytesIO
import xlsxwriter

from .models import (
    Informasi, Kantor, Jabatan, Profile, 
    Perusahaan, Tenaga_kerja
)


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
    else:
        datas = Perusahaan.objects.select_related('username','pembina').filter(pembina__username__username=user)
    context = {
        'datas':datas,
        'profiles':profiles,
        'kepala':kepala,
        'keps':keps,
        'ply':ply,
    }
    return render(request, 'kepesertaan/data_user.html', context)



@csrf_exempt
def Daftar_Pembina(request):
    kd_kantor = request.user.profile_set.values('kode_kantor__pk')[0]['kode_kantor__pk']
    
    nama = request.POST.get('nama_pembina')
    jabatan = request.POST.get('jabatan')
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
            Perusahaan.objects.create(username_id=user.pk,nama=nama, nik=nik, email=email,
                no_hp=no_hp, npp=npp, nama_perusahaan=nama_pers,
                alamat=alamat, desa_kel=desa_kel, kecamatan=kecamatan, kota_kab=kota_kab,
                pembina_id=pembina)

            return JsonResponse({'success':'done'})
        else:
            return JsonResponse({'error':'Password tidak sama!'})
    except:
        return JsonResponse({'error':'Pastikan semua data terisi dan benar!'})

@csrf_exempt
def daftar_perusahaan_admin(request):
    npp = request.POST.get('npp_admin')
    nama_pers = request.POST.get('nama_pemberi_kerja_admin')
    nik = request.POST.get('nik_admin')
    nama = request.POST.get('nama_lengkap_admin')
    pembina = request.POST.get('id_pembina_admin')
    email = request.POST.get('email_admin')
    no_hp = request.POST.get('no_hp_admin')
    alamat = request.POST.get('alamat_perusahaan_admin')
    desa_kel = request.POST.get('desa_kel_admin')
    kecamatan = request.POST.get('kecamatan_admin')
    kota_kab = request.POST.get('kota_kab_admin')
    username = request.POST.get('username_admin')
    password1 = request.POST.get('password1_admin')
    password2 = request.POST.get('password2_admin')

    try:
        if password1 == password2 :
            user = User.objects.create(username=username, password=password1)
            Perusahaan.objects.create(username_id=user.pk,nama=nama, nik=nik, email=email,
                no_hp=no_hp, npp=npp, nama_perusahaan=nama_pers,
                alamat=alamat, desa_kel=desa_kel, kecamatan=kecamatan, kota_kab=kota_kab,
                pembina_id=pembina)

            return JsonResponse({'success':'done'})
        else:
            return JsonResponse({'error':'Password tidak sama!'})
    except:
        return JsonResponse({'error':'Pastikan semua data terisi dan benar!'})
    

def save_to_models(request):
    pembina = request.user.profile_set.values('pk')[0]['pk']
    
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_url = fs.url(filename)
        excel_file = uploaded_url
        
        exceldata = pd.read_excel("."+excel_file)
        
        dbframe = exceldata
        for dbframe in dbframe.itertuples():
            
            user = User.objects.create(username=dbframe.NPP, password=dbframe.NPP)
            obj = Perusahaan.objects.select_related('pembina','username').create(nama=dbframe.NAMA_LENGKAP, nik=dbframe.NIK, email=dbframe.EMAIL,
                no_hp=dbframe.NO_HANDPHONE, npp=dbframe.NPP, nama_perusahaan=dbframe.NAMA_PERUSAHAAN, alamat=dbframe.ALAMAT_PERUSAHAAN,
                desa_kel=dbframe.DESA_KELURAHAN, kecamatan=dbframe.KECAMATAN, kota_kab=dbframe.KOTA_KABUPATEN, username_id=user.pk, pembina_id=pembina)
            obj.save()

        return JsonResponse({'success':'Done'})

def save_to_models_admin(request):
    # pembina = request.user.profile_set.values('pk')[0]['pk']
    
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_url = fs.url(filename)
        excel_file = uploaded_url
        
        exceldata = pd.read_excel("."+excel_file)
        
        dbframe = exceldata
        
        for dbframe in dbframe.itertuples():
            
            user = User.objects.create(username=dbframe.NPP, password=dbframe.NPP)
            obj = Perusahaan.objects.select_related('pembina','username').create(nama=dbframe.NAMA_LENGKAP, nik=dbframe.NIK, email=dbframe.EMAIL,
                no_hp=dbframe.NO_HANDPHONE, npp=dbframe.NPP, nama_perusahaan=dbframe.NAMA_PERUSAHAAN, alamat=dbframe.ALAMAT_PERUSAHAAN,
                desa_kel=dbframe.DESA_KELURAHAN, kecamatan=dbframe.KECAMATAN, kota_kab=dbframe.KOTA_KABUPATEN, username_id=user.pk, pembina_id=dbframe.ID_PEMBINA)
            obj.save()

        return JsonResponse({'success':'Done'})
        # return render(request, 'kepesertaan/upload.html',{'upload_url':uploaded_url})
 
    # return render(request, 'kepesertaan/upload.html')

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
    # try:
    #     datas = Perusahaan.objects.all()[1]
        # npp = datas[0].npp
    # for data in datas:
    worksheet.write(row, col, "BB0400001")
    worksheet.write(row, col+1, "PT NAMA PERUSAHAAN ANDA")
    worksheet.write(row, col+2, "NAMA PIC PERUSAHAAN")
    worksheet.write(row, col+3, "NIK PIC PERUSAHAAN")
    worksheet.write(row, col+4, "HRD")
    worksheet.write(row, col+5,"EMAIL PERUSAHAAN")
    worksheet.write(row, col+6, "NO HP PIC PERUSAHAAN")
    worksheet.write(row, col+7, "ALAMAT PERUSAHAAN")
    worksheet.write(row, col+8, "DESA/KEL PERUSAHAAN")
    worksheet.write(row, col+9, "KECAMATAN PERUSAHAAN")
    worksheet.write(row, col+10, "KOTA/KAB PERUSAHAAN")
    # except:
    #     pass
        
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="uploaded.xlsx"'

    response.write(output.getvalue())
    return response

def download_excel_admin(request):
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
    worksheet.write('L1','ID_PEMBINA', bold)

    row = 1
    col = 0
    # try:
    #     datas = Perusahaan.objects.all()[1]
        # npp = datas[0].npp
    # for data in datas:
    worksheet.write(row, col, "BB0400001")
    worksheet.write(row, col+1, "PT NAMA PERUSAHAAN ANDA")
    worksheet.write(row, col+2, "NAMA PIC PERUSAHAAN")
    worksheet.write(row, col+3, "NIK PIC PERUSAHAAN")
    worksheet.write(row, col+4, "HRD")
    worksheet.write(row, col+5,"EMAIL PERUSAHAAN")
    worksheet.write(row, col+6, "NO HP PIC PERUSAHAAN")
    worksheet.write(row, col+7, "ALAMAT PERUSAHAAN")
    worksheet.write(row, col+8, "DESA/KEL PERUSAHAAN")
    worksheet.write(row, col+9, "KECAMATAN PERUSAHAAN")
    worksheet.write(row, col+10, "KOTA/KAB PERUSAHAAN")
    worksheet.write(row, col+11, "ID PEMBINA")

    worksheet2 = workbook.add_worksheet(name="DAFTAR PEMBINA")
    worksheet2.write('A1','ID',bold)
    worksheet2.write('B1','USER',bold)
    worksheet2.write('C1','NAMA PEMBINA',bold)

    row = 1
    col = 0

    try:
        datas = Profile.objects.select_related('username').all().exclude(jabatan__pk=3)
        for data in datas:
            
            worksheet2.write(row, col, data.id)
            worksheet2.write(row, col+1, data.username.username)
            worksheet2.write(row, col+2, data.nama)
            row += 1
    except:
        pass
    # except:
    #     pass
        
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="uploaded.xlsx"'

    response.write(output.getvalue())
    return response

def informasi(request):

    # user = Profile.objects.select_related('username').filter(username__username=request.user)
    # if user.exists():
    #     datas = Informasi.objects.select_related('npp').filter(npp__pembina__username__username=request.user)
    #     return render(request, 'kepesertaan/informasi.html', {'datas':datas})
    # else:
    #     datas = Informasi.objects.select_related('npp').filter(npp__npp=request.user)
    return render(request, 'kepesertaan/informasi.html')
        
    