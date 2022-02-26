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

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.lib.pagesizes import A4
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

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
            status=Subquery(approval_bak.objects.filter(berita_acara_id=OuterRef('pk')).values('status'))
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
    petugas = request.POST.get('petugas')
    npp = request.POST.get('npp')
    nama = request.POST.get('nama')
    jabatan = request.POST.get('jabatan')
    alamat = request.POST.get('alamat')
    no_hp = request.POST.get('no_hp')
    tujuan = request.POST.get('tujuan')
    lokasi = request.POST.get('lokasi')
    hasil = request.POST.get('hasil')


    profile = Profile.objects.select_related('username').get(username__username=petugas)
    if profile:
        buat_bak = berita_kunjungan.objects.create(petugas_id=profile.id, to_nama=nama, to_jabatan=jabatan,
            to_perusahaan_id=npp, to_alamat=alamat, to_no_hp=no_hp, tujuan=tujuan, hasil=hasil, to_lokasi=lokasi)
        return JsonResponse({'success':'Berita Acara Berhasil di simpan'})
    return JsonResponse({'error':'Gagal Disimpan! Periksa Kembali Data Anda'})

@login_required(login_url='/accounts/login/')
def detail_kunjungan(request,pk):
    data = berita_kunjungan.objects.select_related('petugas').get(pk=pk)

    # datas = (data.petugas.username.username,data.petugas.nama,data.petugas.jabatan.nama_jabatan,data.petugas.kode_kantor.kode_kantor)
    # informan = (data.to_nama,data.to_jabatan,data.to_alamat,data.to_no_hp)

    datas = """
    User : %s
    Jabatan : %s
    Kode Kantor : %s
    """ % (data.petugas.username.username,data.petugas.jabatan.nama_jabatan,data.petugas.kode_kantor.kode_kantor)

    informan = """
    Nama : %s
    Sebagai : %s
    No HP : %s
    """ % (data.to_nama,data.to_jabatan,data.to_no_hp)

    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(datas, image_factory=factory, box_size=10)
    stream1 = BytesIO()
    img.save(stream1)
    svg1 = stream1.getvalue().decode('ISO-8859-1')
    img2 = qrcode.make(informan, image_factory=factory, box_size=10)    
    stream2 = BytesIO()
    img2.save(stream2)
    svg2 = stream2.getvalue().decode('ISO-8859-1')

    
    context = {
        'data':data,
        # 'svg1':svg1,
        # 'svg2':svg2
        'datas':datas,
        'informan':informan
    }

    # return render(request, 'kunjungan/detil_kunjungan.html', context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline;filename="BAK-{data.petugas.username.username}.pdf"'
    response["Content-Transfer-Encoding"] = "binary"

    html_string = render_to_string("kunjungan/detil_kunjungan.html",context,request=request)

    html = HTML(string=html_string, base_url=request.build_absolute_uri())

 
    result = html.write_pdf()


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
    status = request.POST.get('status')
    print(status)
    if datas.exists():
        if status == '1':
            datas.update(status=1)
            return redirect('list-approval')
        if status == '2':
            datas.update(status=2)
            return redirect('list-approval')
        return redirect('dashboard')
        

    
class GeneratePDF(View):
    def get(self, request, pk, *args, **kwargs):
        data = berita_kunjungan.objects.select_related('petugas').get(pk=pk)

        datas = [data.petugas.username.username,data.petugas.nama,data.petugas.jabatan.nama_jabatan,data.petugas.kode_kantor.kode_kantor]
        informan = [data.to_nama, data.to_perusahaan.npp, data.to_jabatan, data.to_no_hp]
        
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(datas, image_factory=factory, box_size=20)
        img2 = qrcode.make(informan, image_factory=factory, box_size=20)
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
        # pdf = render_to_pdf(html)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Detil_Kunjungan_%s.pdf" % (data.created)
            content = "inline; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            #GET RESPONSE
            return response
        return HttpResponse("NOT FOUND")

def docPDF(request,pk):
    data = berita_kunjungan.objects.select_related('petugas').get(pk=pk)
    datas = """
    User : %s
    Nama Petugas : %s
    Jabatan : %s
    Kode Kantor : %s
    """ % (data.petugas.username.username,data.petugas.nama,data.petugas.jabatan.nama_jabatan,data.petugas.kode_kantor.kode_kantor)

    informan = """
    Nama : %s
    Sebagai : %s
    No HP : %s
    """ % (data.to_nama,data.to_jabatan,data.to_no_hp)

    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(datas, image_factory=factory, box_size=10)
    stream1 = BytesIO()
    img.save(stream1)
    svg1 = stream1.getvalue().decode('ISO-8859-1')
    img2 = qrcode.make(informan, image_factory=factory, box_size=10)    
    stream2 = BytesIO()
    img2.save(stream2)
    svg2 = stream2.getvalue().decode('ISO-8859-1')

    
    context = {
        'data':data,
        'svg1':svg1,
        'svg2':svg2
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="berita_kunjungan.pdf"'
    p = canvas.Canvas(response)

    html_string = render_to_string("kunjungan/detil_kunjungan.html",context,request=request)
    p.drawString(0,0, html_string)
    # p.drawString(60, 700, "Ngintil")

    # fecha = str(data.pk)
    # qr_code = qr.QrCodeWidget("TEsting file pdf: " + fecha)
    # bounds = qr_code.getBounds()
    # width = bounds[2] - bounds[0]
    # height = bounds[3] - bounds[1]
    c = Drawing(25, 25, transform=[200, 0, 0, 200, 0, 0])
    # c.add(qr_code)
    renderPDF.draw(c, p, 320, 600)
    p.showPage()
    p.save()
    return response