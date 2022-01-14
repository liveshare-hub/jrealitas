$(document).ready(function(){
    
    $("a").click(function(){
        var data = new FormData()
    data.append("to_user", $(this).text())
    data.append("csrfmiddlewaretoken",$("input[name='csrfmiddlewaretoken']").val())
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
                console.log(size)
                
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