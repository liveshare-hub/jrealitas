function DaftarPembina() {
    var data = new FormData()
    data.append("nama_pembina", $("#nama_pembina").val())
    data.append("jabatan", $('select#makeselect option').filter(':selected').val())
    data.append("kd_user", $("#kd_user").val())
    data.append("kd_kantor", $("#kd_kantor").val())
    data.append("email_pembina",$("#email_pembina").val())
    data.append("no_hp_pembina",$("#no_hp_pembina").val())
    data.append("username", $("#pembaina_username").val())
    data.append("password1", $("#pembina_password1").val())
    data.append("password2", $("#pembina_password2").val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    
    $.ajax({
        method:"POST",
        url:"/create/pembina/",
        contentType:false,
        processData:false,
        data:data,
        success:function(res){
            $("input.clear").val("")
            $('select#makeselect option').val("0")
            
            if(res['error']){
                Swal.fire({
                    icon: 'error',
                    title: 'Error!',
                    text: 'Username sudah terdaftar sebelumnya!',
                    
                  })
            }
            if(res['success']){
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: 'Data Berhasil disimpan',
                    preConfirm: () => {
                        location.reload()
                    }
                  })
            }
            if(res['data_error']){
                Swal.fire({
                    icon: 'error',
                    title: 'Error!',
                    text: 'Password Tidak Sama',
                  })
            }
            
        },
        error:function(err){
            console.log(err)
        }
    })
    
}

$(document).ready(function(){

    $("#kd_user").on("focusout", function() {
        var kd_user = $(this).val()
        $("#pembaina_username").val(kd_user)
    })

    $("#form_register_pembina").validate({
        rules:{
            nama:{
                required:true,
            },
            makeselect:{
                required:true,
            },
            bidang:{
                required:true,
            },
            kd_user:{
                required:true,
                minlength:8,
            },
            email:{
                required:true,
            },
            no_hp:{
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
            nama:{
                required:"Nama tidak boleh kosong",
            },
            makeselect:{
                required:"Jabatan harus dipilih",
            },
            bidang:{
                required:"Bidang harus dipilih!",
            },
            kd_user:{
                required:"Kode user tidak boleh kosong",
            },
            email:{
                required:"Email tidak boleh kosong",
            },
            no_hp:{
                required:"No HP tidak boleh kosong",
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

    $("#daftar_pembina_btn").click(function() {
        DaftarPembina();
    })
})