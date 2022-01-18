function createThread(el){
    var data = new FormData()
    data.append("to_user", el)
    $.ajax({
        method:"POST",
        url:'/chat/create/thread/',
        data:data,
        contentType:false,
        processData:false,
        success:function(data){
            const obj = JSON.parse(data.data)

            html = `<p class="hidden" data=${obj[0].pk} data-user=${obj[0].fields.to_user} id="id_thread"></p>`
            $("#sender").append(html)
        },
        error:function(err){
            console.log(err)
        },
    })
}

$(document).ready(function(){
    $("#kirim_pesan").click(function(){
        var data = new FormData()
        data.append("pesan",$("#pesan_id").text())
        data.append("thread_id",$("p#id_thread").attr('data'))
        data.append("to_user",$("p#id_thread").attr('data-user'))

        $.ajax({
            method:'POST',
            url:'/chat/save/chat/',
            dataType:"json",
            data:data,
            contentType:false,
            processData:false,
            success:function(data){
                $("#pesan_id").text("")
                console.log(data)
            },
            error:function(err){
                console.log(err)
            }
        })
        
    })
    // $("div#pesan_id").focusout(function(){ 
    //     console.log($(this).text())
    // })
    $("a").click(function(){

        createThread($(this).text())
        $("p.hidden").remove()
        var data = new FormData()
        data.append("to_user", $(this).text())
    // data.append("csrfmiddlewaretoken",$("input[name='csrfmiddlewaretoken']").val())
        $.ajax({
            method:"POST",
            url:'/chat/load/chat/',
            dataType:"json",
            data:data,
            contentType:false,
            processData:false,
            success:function(data){
                
                let html = '';
                var size = Object.keys(data).length;
                
               for (let count = 0; count < size; count++) {
                  const obj = JSON.parse(data.data)
                  html += '<div class="row" style="margin-left:0; margin-right:0"><div class="col-md">';
                  if (data.data.sender_id === $("p").attr('data')) {
                     html += '<div class="row"><div align="left" class="col-md"><span class = "text-muted"><small><b>' + obj[0].fields.date + '</b></small></span></div></div>';
                     html += '<div class="row"><div align="left" class="col-md-8 alert alert-secondary">';
                  } else {
                     html += '<div class="row"><div align="right" class="col-md"><span class = "text-muted"><small><b>' + obj[0].fields.date + '</b></small></span></div></div>';
                     html += '<div class="row justify-content-end"><div align="right" class="col-md-8  alert alert-success">';
                  }
                  html += '<div style="font-size:14px;">' + obj[0].fields.body + '</div></div></div></div></div>';
               }
               $("#id_pesan").html(html)
            },
            error:function(err){
                console.log(err)
            }
        })
    })


})