function DafarNPP() {
    var data = new FormData()
    data.append("npp", $("#npp").val())
    data.append("nama_pemberi_kerja", $("#nama_pemberi_kerja").val())
    data.append("nik", $("#nik").val())
    data.append("nama_lengkap", $("#nama_lengkap").val())
    data.append("jabatan", $('select#makeselect option').filter(':selected').val())
    data.append("pembina_id", $("#pembina_id").val())
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
        url:"/create/npp/",
        contentType:false,
        processData:false,
        data:data,
        success:function(res){
            $("input").val("")
            $("#makeselect").val("7")
            
            console.log(res['success'])
            
        },
        error:function(err){
            console.log(err)
        }
    })
}

function uploadFile() {

    var data = new FormData()
    data.append("file", $("#file")[0].files[0])
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    $.ajax({
        method:"POST",
        url:"/templates/upload/",
        contentType:false,
        mimeType:"multipart/form-data",
        processData:false,
        data:data,
        success:function(data){
            console.log(data)
            location.href = "/user/data/"
           
        },
        error:function(err){
            console.log(err)
        }
    })

}

$(document).ready(function() {
    $("#form_registrasi_user_perusahaan").validate({
        rules:{
            npp:{
                required:true,
            },
            nama_pemberi_kerja:{
                required:true,
            },
            nik:{
                required:true,
            },
            nama_lengkap:{
                required:true,
            },
            email:{
                required:true,
            },
            no_hp:{
                required:true,
            },
            alamat_perusahaan:{
                required:true,
            },
            desa_kel:{
                required:true,
            },
            kecamatan:{
                required:true,
            },
            kota_kab:{
                required:true,
            },
            password1:{
                required:true,
                minlength:8,
            },
            password2:{
                required:true,
                minlength:8,
                equalTo:"#password1"
            }
        },
        messages:{
            npp:{
                required:"NPP tidak boleh kosong!",
            },
            nama_pemberi_kerja:{
                required:"Nama perusahaan tidak boleh kosong!",
            },
            nik:{
                required:"NIK tidak boleh kosong",
            },
            nama_lengkap:{
                required:"Nama tidak boleh kosong",
            },
            email:{
                required:"Email tidak boleh kosong",
            },
            no_hp:{
                required:"No HP tidak boleh kosong",
            },
            alamat_perusahaan:{
                required:"Alamat tidak boleh kosong",
            },
            desa_kel:{
                required:"Desa/Kelurahan tidak boleh kosong",
            },
            kecamatan:{
                required:"Kecamatan tidak boleh kosong",
            },
            kota_kab:{
                required:"Kota/Kabupaten tidak boleh kosong",
            },
            password1:{
                required:"Passowrd tidak boleh kosong",
                minlength:"Password minimal harus 8 karakter",
            },
            password2:{
                required:"Password Konfirmasi tidak boleh kosong",
                minlength:"Password minimal harus 8 karakter",
                equalTo:"Password harus sama dengan password di atas"
            }  
        },
    })

    $("#daftar").click(function(){
        
        $("#form_registrasi_user_perusahaan").valid();
        DafarNPP();
    })

    $("#upload").click(function(e) {
      //  e.preventDefault();
        uploadFile();
    })

})
    