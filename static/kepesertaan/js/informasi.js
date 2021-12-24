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
    
    $("#id_check_npp").hide();
    $("#id_kirim_ke_npp").on('change',function(){
       
        if($(this).val() === '2'){
            $("#id_tbl_check_npp > tbody").show();
            $("#id_check_npp").show();
            
        }else{
            $("#id_tbl_check_npp > tbody").hide("")
            $("#id_check_npp").hide();
        }
        
    })

    $("#id_kirim_informasi").on('submit',function(){
        var data = new FormData()
        data.append("judul",$("#id_judul").val())
        data.append("isi",$("#id_isi").val())
        data.append("file",$("#id_attachment")[0].files[0])

    })
})