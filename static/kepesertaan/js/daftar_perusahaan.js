var profileQuery = `query{
    allProfile{
      id
      username{
        id
        username
      }
    }
}`

function DafarNPP() {
    console.log($("#npp").val())
    var data = new FormData()
    data.append("npp", $("#npp").val())
    data.append("nama_pemberi_kerja", $("#nama_pemberi_kerja").val())
    //data.append("nik", $("#nik").val())
    data.append("nama_lengkap", $("#nama_lengkap").val())
    //data.append("jabatan", $('select#makeselect option').filter(':selected').val())
    data.append("pembina_id", $("#pembina_id").val())
    //data.append("email",$("#email").val())
    //data.append("no_hp",$("#no_hp").val())
    //data.append("nama_pemilik",$("#nama_pemilik").val())
    //data.append("npwp",$("#npwp").val())
    //data.append("alamat_perusahaan",$("#alamat_perusahaan").val())
    //data.append("desa_kel",$("#desa_kel").val())
    //data.append("kecamatan", $("#kecamatan").val())
    //data.append("kota_kab",$("#kota_kab").val())
    //data.append("kode_pos",$("#kode_pos").val())
    data.append("username", $("#username").val())
    //data.append("password1", $("#password1").val())
    //data.append("password2", $("#password2").val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    
    $.ajax({
        method:"POST",
        url:"/create/npp/",
        contentType:false,
        processData:false,
        data:data,
        success:function(res){
            //$("input").val("")
            //$("#makeselect").val("7")
            window.location = '/'
            console.log(res['success'])
            
        },
        error:function(err){
            console.log(err)
        }
    })
}

function DafarNPPAdmin() {
    var data = new FormData()
    data.append("npp_admin", $("#npp_admin").val())
    data.append("nama_pemberi_kerja_admin", $("#nama_pemberi_kerja_admin").val())
    data.append("nik_admin", $("#nik_admin").val())
    data.append("nama_lengkap_admin", $("#nama_lengkap_admin").val())
    data.append("jabatan_perusahaan_admin", $("#jabatan_perusahaan_admin").val())
    data.append("id_pembina_admin", $('select#id_pembina_admin option').filter(':selected').val())
    data.append("id_jabatan", $("#id_jabatan").val())
    data.append("email_admin",$("#email_admin").val())
    data.append("no_hp_admin",$("#no_hp_admin").val())
    data.append("nama_pemilik_admin",$("#nama_pemilik_admin").val())
    data.append("npwp_admin",$("#npwp_admin").val())
    data.append("alamat_perusahaan_admin",$("#alamat_perusahaan_admin").val())
    data.append("desa_kel_admin",$("#desa_kel_admin").val())
    data.append("kecamatan_admin", $("#kecamatan_admin").val())
    data.append("kota_kab_admin",$("#kota_kab_admin").val())
    data.append("kode_pos_admin",$("#kode_pos_admin").val())
    data.append("username_admin", $("#username_admin").val())
    data.append("password1_admin", $("#password1_admin").val())
    data.append("password2_admin", $("#password2_admin").val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    

    $.ajax({
        method:"POST",
        url:"/create/npp/",
        contentType:false,
        processData:false,
        data:data,
        success:function(res){
            
            $("input.clear").val("")
            $("#id_pembina_admin").val(0)
            
            
        },
        error:function(err){
            console.log(err)
        }
    })
}

function DaftarPembina() {
    var data = new FormData()
    data.append("nama_pembina", $("#nama_pembina").val())
    data.append("jabatan", $('select#makeselect option').filter(':selected').val())
    data.append("kd_user", $("#kd_user").val())
    data.append("kepala_id", $("#id_jabatan_pembina").val())
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
                swal({
                    icon: 'error',
                    title: 'Error!',
                    text: 'Username sudah terdaftar sebelumnya!',
                    
                  })
            }
            if(res['success']){
                swal({
                    icon: 'success',
                    title: 'Success',
                    text: 'Data Berhasil disimpan',
                  })
            }
            if(res['data_error']){
                swal({
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

function resetPassword(){
    var pk = $("#id_ganti_password_pembina").val()
    var data = new FormData()
    data.append("id_pembina",$("#id_ganti_password_pembina").val())
    data.append("password1", $("#id_edit_password1").val())
    data.append("password2",$("#id_edit_password2").val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    $.ajax({
        method:"POST",
        url:`/ganti/password/${pk}`,
        contentType:false,
        processData:false,
        data:data,
        success:function(data){
            location.href = "/user/data/"
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
            
            location.href = "/user/data/"
           
        },
        error:function(err){
            console.log(err)
        }
    })

}

function uploadFileAdmin() {

    var data = new FormData()
    data.append("file", $("#upload_user_perusahaan_admin")[0].files[0])
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    $.ajax({
        method:"POST",
        url:"/templates/admin/upload/",
        contentType:false,
        mimeType:"multipart/form-data",
        processData:false,
        data:data,
        success:function(data){
            
            location.href = "/user/data/"
           
        },
        error:function(err){
            console.log(err)
        }
    })

}


function uploadTK(){
    var data = new FormData()
    data.append("file",$("#file_tk")[0].files[0])
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    $.ajax({
        method:"POST",
        url:"/templates/tk/upload/",
        contentType:false,
        mimeType:"multipart/form-data",
        processData:false,
        data:data,
        success:function(data){
            location.href = "/user/data/"
        },
        error:function(err){
            console.log(err)
        }
    })
}

function updateBinaan(){
    console.log($("#id_npp_pindah").attr('data-npp'))
    console.log($('select#selectpembina option').filter(':selected').val())
    var data = new FormData()
    data.append("npp", $("#id_npp_pindah").attr('data-npp'))
    data.append("pembina", $('select#selectpembina option').filter(':selected').val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    $.ajax({
        method:"POST",
        url:"/pindah/binaan/",
        contentType:false,
        processData:false,
        data:data,
        success:function(data){
            console.log(data)
            
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

    $("#form_registrasi_user_perusahaan_admin").validate({
        rules:{
            npp_admin:{
                required:true,
            },
            nama_pemberi_kerja_admin:{
                required:true,
            },
            nik_admin:{
                required:true,
            },
            nama_lengkap_admin:{
                required:true,
            },
            email_admin:{
                required:true,
            },
            no_hp_admin:{
                required:true,
            },
            id_pembina_admin:{
                required:true,
            },
            alamat_perusahaan_admin:{
                required:true,
            },
            desa_kel_admin:{
                required:true,
            },
            kecamatan_admin:{
                required:true,
            },
            kota_kab_admin:{
                required:true,
            },
            password1_admin:{
                required:true,
                minlength:8,
            },
            password2_admin:{
                required:true,
                minlength:8,
                equalTo:"#password1"
            }
        },
        messages:{
            npp_admin:{
                required:"NPP tidak boleh kosong!",
            },
            nama_pemberi_kerja_admin:{
                required:"Nama perusahaan tidak boleh kosong!",
            },
            nik_admin:{
                required:"NIK tidak boleh kosong",
            },
            nama_lengkap_admin:{
                required:"Nama tidak boleh kosong",
            },
            email_admin:{
                required:"Email tidak boleh kosong",
            },
            no_hp_admin:{
                required_admin:"No HP tidak boleh kosong",
            },
            id_pembina_admin:{
                required:"Pembina tidak boleh kosong",
            },
            alamat_perusahaan_admin:{
                required_admin:"Alamat tidak boleh kosong",
            },
            desa_kel_admin:{
                required:"Desa/Kelurahan tidak boleh kosong",
            },
            kecamatan_admin:{
                required:"Kecamatan tidak boleh kosong",
            },
            kota_kab_admin:{
                required:"Kota/Kabupaten tidak boleh kosong",
            },
            password1_admin:{
                required:"Passowrd tidak boleh kosong",
                minlength:"Password minimal harus 8 karakter",
            },
            password2_admin:{
                required:"Password Konfirmasi tidak boleh kosong",
                minlength:"Password minimal harus 8 karakter",
                equalTo:"Password harus sama dengan password di atas"
            }  
        },
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

    $("#daftar").click(function(){
        
        $("#form_registrasi_user_perusahaan").valid();
        DafarNPP();
    })

    $("#daftar_admin").click(function() {
        $("#form_registrasi_user_perusahaan_admin").valid();
        DafarNPPAdmin();
    })

    $("#reset_password").click(function() {
        resetPassword();
    })

    $("#upload").click(function(e) {
      //  e.preventDefault();
        uploadFile();
    })

    $("#upload_admin").click(function() {
        //  e.preventDefault();
        uploadFileAdmin();
      })

    $("#jabatan_pembina").on('change', function(){

    })

    $("#daftar_pembina_btn").click(function() {
        DaftarPembina();
    })

    $("#update_binaan").click(function() {
        updateBinaan();
    })

    var pk = $("#id_ganti_password").val()
    $(`#form_edit_password${pk}`).submit(function() {
        
        var data = new FormData()
        data.append("edit_password1",$("#id_edit_password1").val())
        data.append("edit_password2",$("#id_edit_password2").val())
        data.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val())

        $.ajax({
            method:'POST',
            url:`/ganti/password/${pk}`,
            contentType:false,
            processData:false,
            data:data,
            success:function(res){
                console.log(res)
                if(res['status'] === 200){
                    $("#warning").remove()
                    $("#alert").append(
                        '<div class="alert alert-success" role="alert" id="success">'+
                        'Password Berhasil Dirubah'+
                      '</div>'
                    )
                    $("#success").fadeOut(5000)
                }else{
                    $("#success").remove()
                    $("#alert").append(
                        '<div class="alert alert-warning" role="alert" id="warning">'+
                        'Password tidak sama'+
                        '</div>'
                      
                    )
                    $("#warning").fadeOut(5000)
                }
                
            },
            error:function(err){
                console.log(err)
            }
        });
        
        $("#id_edit_password1").val("")
        $("#id_edit_password2").val("")
    });
    $.ajax({
        method:"POST",
        url:"/graphql",
        contentType:"application/json",
        data:JSON.stringify({
            query:profileQuery,
        }),
        dataType:"json",
        success:function(data){
            var datas = data['data']['allProfile']

            $.each(datas, function(i,j){

                $("#id_pembina_admin").append($('<option>', {
                    
                    value:j['id'],
                    text:j['username']['username'],       
                }));
            })
          
        },
        error:function(err){
            console.log(err)
        }
    });

    $("#upload_tk").click(function(){
        uploadTK();
    })
});
    

$.fn.modal.Constructor.prototype._enforceFocus = function () {}

$('#myModal').modal()

const pk = $("#delete_pembina").attr('data-pk')
const username = $("#delete_pembina").attr('data-user')

$('#delete_pembina').on('click', function () {
  Swal.fire({
    title: 'PERINGATAN!',
    text: `Hapus user ${username} ?`,
    buttonsStyling: false,
    showCancelButton: true,
    customClass: {
      confirmButton: 'btn btn-sm btn-primary',
      cancelButton: 'btn btn-sm btn-danger',
      loader: 'custom-loader'
    },
    loaderHtml: '<div class="spinner-border text-primary"></div>',
    preConfirm: () => {
      Swal.showLoading()
      return new Promise((resolve) => {
        $.ajax({
            method:'POST',
            url:`/hapus/user/${pk}`,
            success:function(data){
                setTimeout(() => {
                    resolve(true)
                  }, 3000)
                console.log(data)
            },
            error:function(err){
                console.log(err)
            }
        })
      })
    }
  })
})