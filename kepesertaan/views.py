from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

import pandas as pd
from io import StringIO, BytesIO
import xlsxwriter

from .models import (
    Kantor, Jabatan, Profile, 
    Perusahaan, Tenaga_kerja
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
            # user_prof = User_Profile.objects.create(username_id=user.pk, nama=nama, nik=nik,
            #     email=email, no_hp=no_hp)
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

    datas = Perusahaan.objects.filter(npp="BB0409090").all()
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

    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    npp = datas[0].npp
    response['Content-Disposition'] = f'attachment;filename="{npp}.xlsx"'

    response.write(output.getvalue())
    return response