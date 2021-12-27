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
    var nppArr = new Array()
    $("#id_check_npp").hide();
    $("#id_kirim_ke_npp").on('change',function(){
       
        if($(this).val() === '2'){
            $("#id_tbl_check_npp > tbody").show();
            $("#id_check_npp").show();
            // $("#id_kirim_informasi").on('submit', function(){
            //     var 
            // })
            
            
        }else if($(this).val() === '1'){
            $("#id_tbl_check_npp > tbody").hide("")
            $("#id_check_npp").hide();
        }else{
            $("#id_tbl_check_npp > tbody").hide("")
            $("#id_check_npp").hide();
            
        }
        
    })

    $("#id_submit_info").on('click', function(){
        console.log($("#id_attachment")[0].files[0])
        var data = new FormData()
        data.append("judul",$("#id_judul").val())
        data.append("isi",$("#id_isi").val())
        data.append("attach",$("#id_attachment")[0].files[0])
        data.append("user",$("#user_name").text())
        data.append("csrfmiddlewaretoken",$("input[name=csrfmiddlewaretoken]").val())

        $.ajax({
            method:"POST",
            url:'/informasi/create/user/ajax',
            contentType:false,
            processData:false,
            data:data,
            success:function(res){
                console.log(res)
            },
            errors:function(err){
                console.log(err)
            }
        })
    })
})