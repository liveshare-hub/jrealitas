var nppQuery = `
query{
    allNpp{
      id
      npp
      namaPerusahaan
    }
  }
`
var data="";


$(document).ready(function(){

    $("#id_kirim_informasi").validate({
       
        rules:{
            judul:{
                required:true
            },
            isi:{
                required:true
            },
            attachment:{
                required:true
            }
        },
        messages:{
            judul:{
                required:"Judul Tidak boleh kosong"
            },
            isi:{
                required:"Isi tidak boleh kosong"
            },
            attachment:{
                required:"File tidak boleh kosong"
            }
        }
    })
    
    $("#id_check_npp").hide();
    
    $("#id_kirim_ke_npp").on('change',function(){
       
        if($(this).val() === '2'){
            $("#id_submit_info").removeAttr("disabled")
            $("#id_tbl_check_npp > tbody").show();
            $("#id_check_npp").show();
            $("#id_submit_info").on('click', function(){
                formValid = $("#id_kirim_informasi").valid();
                if(formValid){
                    var data = new FormData()
                
                    data.append("judul",$("#id_judul").val())
                    data.append("isi",$("#id_isi").val())
                    data.append("attach",$("#id_attachment")[0].files[0])
                    data.append("user",JSON.stringify($('input[name="cek_npp"]:checked').serializeArray()))
                    data.append("csrfmiddlewaretoken",$("input[name=csrfmiddlewaretoken]").val())
        
                    $.ajax({
                        method:"POST",
                        url:'/informasi/create/user/ajax',
                        contentType:false,
                        processData:false,
                        data:data,
                        success:function(res){
                            $("#id_judul").val("")
                            $("#id_isi").val("")
                            $("#id_attachment").val(null)
                            $("#id_kirim_ke_npp").val("0")
                        },
                        errors:function(err){
                            console.log(err)
                        }
                    })

                }
                
            })
            
            
        }else if($(this).val() === '1'){
            $("#id_submit_info").removeAttr("disabled")
            $("#id_tbl_check_npp > tbody").hide("")
            $("#id_check_npp").hide();
            $("#id_submit_info").on('click', function(){
                formValid = $("#id_kirim_informasi").valid();
                if(formValid){
                    var data = new FormData()
                
                    data.append("judul",$("#id_judul").val())
                    data.append("isi",$("#id_isi").val())
                    data.append("attach",$("#id_attachment")[0].files[0])
                    data.append("user",JSON.stringify($('input[name="cek_npp"]:checked').serializeArray()))
                    data.append("csrfmiddlewaretoken",$("input[name=csrfmiddlewaretoken]").val())
        
                    $.ajax({
                        method:"POST",
                        url:'/informasi/create/user/ajax',
                        contentType:false,
                        processData:false,
                        data:data,
                        success:function(res){
                            $("#id_judul").val("")
                            $("#id_isi").val("")
                            $("#id_attachment").val(null)
                            $("#id_kirim_ke_npp").val("0")
                            
                        },
                        errors:function(err){
                            console.log(err)
                        }
                    })

                }
        
               
            })

        }else{
            $("#id_submit_info").attr("disabled",true)
            $("#id_tbl_check_npp > tbody").hide("")
            $("#id_check_npp").hide();
            
        }
        
    })

    // $("#id_submit_info").on('click', function(){
        
    //     var data = new FormData()
    //         data.append("judul",$("#id_judul").val())
    //         data.append("isi",$("#id_isi").val())
    //         data.append("attach",$("#id_attachment")[0].files[0])
    //         data.append("user",JSON.stringify($('input[name="cek_npp"]:checked').serializeArray()))
    //         data.append("csrfmiddlewaretoken",$("input[name=csrfmiddlewaretoken]").val())

    //         $.ajax({
    //             method:"POST",
    //             url:'/informasi/create/user/ajax',
    //             contentType:false,
    //             processData:false,
    //             data:data,
    //             success:function(res){
    //                 console.log(res)
    //             },
    //             errors:function(err){
    //                 console.log(err)
    //             }
    //         })
    // })
})