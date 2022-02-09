var NppPembinaQuery = `
query{
    allNppPembina{
      id
      npp
    }
  }
`


function SimpanKunjungan(){
    var data = new FormData()
    data.append("nama",$("#id_to_nama").val())
    data.append("npp", $('select#id_npp option').filter(':selected').val())
    data.append("jabatan",$("#id_to_jabatan").val())
    data.append("alamat",$("#id_to_alamat").val())
    data.append("no_hp",$("#id_to_no_hp").val())
    data.append("petugas",$("#id_petugas").val())
    data.append("hasil",$("#id_hasil").val())
    data.append("lokasi",$("#id_to_lokasi").val())
    data.append("tujuan", $('select#id_tujuan option').filter(':selected').val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())

    $.ajax({
        method:'POST',
        url:'/kunjungan/buat/',
        contentType:false,
        processData:false,
        data:data,
        success:function(res){
            // var notif = res['success']
            
            // $("#id_to_nama").val("")
            // $("#id_to_jabatan").val("")
            // $("#id_to_alamat").val("")
            // $("#id_to_no_hp").val("")
            // $("#id_to_lokasi").val("")
            // $("#id_tujuan").val("0")
            // $("#id_npp").val("0")
            // $("#id_hasil").val("")
            location.href = '/kunjungan/'
        },
        error:function(err){
            console.log(err)
        }
    })
}

$("#id_buat").click(function(){
    SimpanKunjungan();
})

$(document).ready(function(){
    $.ajax({
        method:'POST',
        url:'/graphql',
        contentType:"application/json",
        data:JSON.stringify({
          query:NppPembinaQuery,
        }),
        dataType:"json",
        success:function(data){
          users = data['data']['allNppPembina']
          
          $.each(users, function(user,index) {
            
            $("#id_npp").append($('<option>', {
              value:index['id'],
              text:index['npp']
            }));
          });
        },
        error:function(err){
          console.log(err)
        }
      })
})