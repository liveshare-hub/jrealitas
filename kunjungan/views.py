# import os

# os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")


from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string, get_template
from django.views.generic import View
from weasyprint import HTML

import tempfile
# import pdfkit
import qrcode
import qrcode.image.svg
from io import BytesIO


from kepesertaan.models import Profile
from .models import berita_kunjungan, approval_bak

from .form import KunjunganForm
from .utils import render_to_pdf

@login_required(login_url='/accounts/login/')
def kunjungan(request):
    user = request.user
    profile = Profile.objects.select_related('username').get(username__username=user)
    
    # print(profile.pk)
    if profile:
        data_kunjungan = berita_kunjungan.objects.select_related('petugas').filter(petugas__username__username=profile.username).annotate(
            status_approve=Subquery(approval_bak.objects.filter(berita_acara_id=OuterRef('pk')).values('approved'))
        )
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
    npp = request.POST['npp']
    nama = request.POST['nama']
    jabatan = request.POST['jabatan']
    alamat = request.POST['alamat']
    no_hp = request.POST['no_hp']
    tujuan = request.POST['tujuan']
    lokasi = request.POST['lokasi']
    hasil = request.POST['hasil']

    profile = Profile.objects.select_related('username').get(username__username=petugas)
    if profile:
        buat_bak = berita_kunjungan.objects.create(petugas_id=profile.pk, to_nama=nama, to_jabatan=jabatan,
            to_perusahaan_id=npp, to_alamat=alamat, to_no_hp=no_hp, tujuan=tujuan, hasil=hasil, to_lokasi=lokasi)
        return JsonResponse({'success':'Berita Acara Berhasil di simpan'})
    return JsonResponse({'error':'Gagal Disimpan! Periksa Kembali Data Anda'})

@login_required(login_url='/accounts/login/')
def detail_kunjungan(request,pk):
    data = berita_kunjungan.objects.select_related('petugas').get(pk=pk)

    datas = [data.petugas.username.username,data.petugas.nama,data.petugas.jabatan.nama_jabatan,data.petugas.kode_kantor.kode_kantor]
    informan = [data.to_nama,data.to_jabatan,data.to_alamat,data.to_no_hp]

    # factory = qrcode.image.svg.SvgImage
    # img = qrcode.make(datas, image_factory=factory, box_size=10)
    # img2 = qrcode.make(informan, image_factory=factory, box_size=10)
    # stream1 = BytesIO()
    # stream2 = BytesIO()
    # img.save(stream1)
    # img2.save(stream2)
    # svg1 = stream1.getvalue().decode()
    # svg2 = stream2.getvalue().decode()
    
    qr1 = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr2 = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr1.add_data(datas)
    qr2.add_data(informan)
    
    qr1.make(fit=True)
    qr2.make(fit=True)

    svg1 = qr1.make_image(fill_color="black", back_color="white")
    svg2 = qr1.make_image(fill_color="black", back_color="white")

    


    context = {
        'data':data,
        'svg1':svg1,
        'svg2':svg2
    }


    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline;filename="BAK-{data.petugas.username.username}.pdf"'
    response["Content-Transfer-Encoding"] = "binary"

    html_string = render_to_string("kunjungan/detil_kunjungan.html",context,request=request)
    # result = pdfkit.from_string(html_string, f'BAK_{data.petugas.username.username}')
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    # html = HTML(string=html_string, base_url=".", url_fetcher=default_url_fetcher)
    result = html.write_pdf()

    # logger = logging.getLogger('weasyprint')
    # logger.addHandler(logging.FileHandler('/Temp/weasyprint.log'))

    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response
    

@login_required
def daftar_approval_kunjungan(request):

    datas = approval_bak.objects.select_related('berita_acara').filter(berita_acara__to_perusahaan__npp=request.user)
    context = {
        'datas':datas
    }
    return render(request, 'kunjungan/approval.html',context)


@login_required
@csrf_exempt
def approval_kunjungan(request, pk):
    datas = approval_bak.objects.select_related('berita_acara').filter(pk=pk)
    if datas.exists():
        datas.update(approved=True)
        

    
class GeneratePDF(View):
    def get(self, request, pk, *args, **kwargs):
        data = berita_kunjungan.objects.select_related('petugas').get(pk=pk)

        datas = [data.petugas.username.username,data.petugas.nama,data.petugas.jabatan.nama_jabatan,data.petugas.kode_kantor.kode_kantor]
        informan = [data.to_nama,data.to_jabatan,data.to_alamat,data.to_no_hp]
        print(datas)
        print(informan)
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(datas, image_factory=factory, box_size=10)
        img2 = qrcode.make(informan, image_factory=factory, box_size=10)
        stream1 = BytesIO()
        stream2 = BytesIO()
        img.save(stream1)
        img2.save(stream2)
        svg1 = stream1.getvalue().decode()
        svg2 = stream2.getvalue().decode()
        template = get_template('kunjungan/detil_kunjungan.html')
        context = {
            'data':data,
            'svg1':svg1,
            'svg2':svg2
        }
        html = template.render(context)
        pdf = render_to_pdf('kunjungan/detil_kunjungan.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Detil_Kunjungan_%s.pdf" % (data.created)
            content = "inline; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return content
        return HttpResponse("NOT FOUND")