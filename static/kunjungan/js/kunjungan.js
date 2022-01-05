function SimpanKunjungan(){
    var data = new FormData()
    data.append("nama",$("#id_to_nama").val())
    data.append("jabatan",$("#id_to_jabatan").val())
    data.append("alamat",$("#id_to_alamat").val())
    data.append("no_hp",$("#id_to_no_hp").val())
    data.append("petugas",$("#id_petugas").val())
    data.append("hasil",$("#id_hasil").val())
    data.append("tujuan", $('select#id_tujuan option').filter(':selected').val())
    data.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())

    $.ajax({
        method:'POST',
        url:'/kunjungan/buat/',
        contentType:false,
        processData:false,
        data:data,
        success:function(res){
            var notif = res['success']

            var myModal = new bootstrap.Modal(document.getElementById("exampleModal"), {});
            console.log(myModal)
            document.onreadystatechange = function () {
            myModal.show();
            $(".modal-body").append(notif)
            };
            
            $("#id_to_nama").val("")
            $("#id_to_jabatan").val("")
            $("#id_to_alamat").val("")
            $("#id_to_no_hp").val("")
            $("#id_tujuan").val("0")
            $("#id_hasil").val("")
        },
        error:function(err){
            console.log(err)
        }
    })
}

$("#id_buat").click(function(){
    SimpanKunjungan();
})