function DaftarPerusahaan() {

    var data = new FormData()
    data.append("npp", $("#npp").val())
    data.append("nama_pemberi_kerja", $("#nama_pemberi_kerja").val())
    data.append("nik", $("#nik").val())
    data.append("nama_lengkap", $("#nama_lengkap").val())
    data.append("jabatan", $('select#makeselect option').filter(':selected').val())
    data.append("pembina", $("#pembina_id").val())
    data.append("email",$("#email").val())
    data.append("no_hp",$("#no_hp").val())
    data.append("alamat_perusahaan",$("#alamat_perusahaan").val())
    data.append("desa_kel",$("#desa_kel").val())
    data.append("kecamatan", $("#kecamatan").val())
    data.append("kota_kab",$("#kota_kab").val())
    data.append("username", $("#username").val())
    data.append("password1", $("#password1").val())
    data.append("password2", $("#password2").val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())

    $.ajax({
        method:"POST",
        contentType:false,
        processData:false,
        data:data,
        success:function(res){
            $("#input").val("")
            $("#makeselect").val("7")
            console.log(res)
            
        },
        error:function(err){
            console.log(err)
        }
    })
}