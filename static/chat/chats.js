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
            var obj = data.data
            // var obj = JSON.parse(data.data)
            html = `<p class="hidden" data-thread=${obj[0].pk} data-user=${obj[0].user__pk} data-to-user=${obj[0].to_user__pk} id="id_thread"></p>`
            pesan = `<p class="mt-2" id="username_id">${obj[0].to_user__username}</p>`
            
            $("#sender").after(html)
            $("p#sender").after(pesan)
            loadChat($("p#id_thread").attr('data-thread'))
        },
        error:function(err){
            console.log(err)
        },
    })
}

function loadChat(el){
    let from = $("p#id_thread").attr('data-user')
    var username = $("p#sender").text();
    let recipent = $("p#id_thread").attr('data-to-user')
    // console.log(recipent, sender)
    
    var data = new FormData()
        data.append("thread_id", el)
        $.ajax({
            method:"POST",
            url:'/chat/load/chat/',
            dataType:"json",
            data:data,
            contentType:false,
            processData:false,
            success:function(data){
                // const obj = JSON.parse(data.data)
                const obj = data.data;
                let html = '';
                // var size = Object.keys(obj).length;
                var size = obj.length;
                
                for (let count = 0; count < size; count++) {
                
                    html += '<div class="row" style="margin-left:0; margin-right:0"><div class="col-md">';
                    var d = new Date(obj[count].date)
                    var tgl = d.getDate()+'-'+String(d.getMonth()+1).padStart(2,"0")+'-'+d.getFullYear()+' '+d.getHours()+':'+String(d.getMinutes()).padStart(2,"0")
                    if (obj[count].user__username === username) {
                        
                        html += '<div class="time sender">'+ tgl +'</div><div class="message sender">'+ obj[count].body+'</div></div></div>'
                        // html += '<div class="row"><div align="right" class="col-md"><span class = "text-muted"><small><b>' + tgl + '</b></small></span></div></div>';
                        // html += '<div class="row justify-content-end"><div align="right" class="col-md-8 alert alert-success">';
                        // html += '<div style="font-size:14px;">' + obj[count].body + '</div></div></div></div></div>'; 
                    }
                //   if(obj[count].fields.recipent == parseInt(recipent)){
                //     html += '<div class="row"><div align="right" class="col-md"><span class = "text-muted"><small><b>' + obj[count].fields.date + '</b></small></span></div></div>';
                //     html += '<div class="row"><div align="right" class="col-md-8 alert alert-primary">';
                //     html += '<div style="font-size:14px;">' + obj[count].fields.body + '</div></div></div></div></div>';
                //   }
                    else {
                        $("#username_id").val(recipent)
                        html += '<div class="time">'+ tgl +'</div><div class="message '+obj[count].recipent__username +'">'+ obj[count].body+'</div></div></div>'
                        // html += '<div class="row"><div align="left" class="col-md"><span class = "text-muted"><small><b>' + tgl + '</b></small></span></div></div>';
                        // html += '<div class="row"><div align="left" class="col-md-8  alert alert-secondary">';
                        // html += '<div style="font-size:14px;">' + obj[count].body + '</div></div></div></div></div>';
                    }
                  
               }
               $("#id_pesan").html(html)
            },
            error:function(err){
                console.log(err)
            }
        })
}

function loadChatAll(){
    loadChat($("p#id_thread").attr('data-thread'))
}

var pesan = document.getElementById("pesan_id")

$(document).ready(function(){
    let sender = $("#sender").text()
    let toUser = $("#to_user").text()
    $("#kirim_pesan").attr('disabled',true)
    $("#pesan_id").on("focusout",function(){
        if($(this).text !== ""){
            $("#kirim_pesan").attr('disabled',false)
        }else{
            $("#kirim_pesan").attr('disabled',true)
        }
    })
    $("#kirim_pesan").click(function(){
        
        if(pesan.textContent !== ""){
            
            $(this).attr('disabled',false)
            var data = new FormData()
            data.append("pesan",$("#pesan_id").text())
            data.append("thread_id",$("p#id_thread").attr('data-thread'))
            // data.append("to_user",$("p#id_thread").attr('data-to-user'))
            data.append("to_user",$("a#to_user").attr('data-user'))
    
            $.ajax({
                method:'POST',
                url:'/chat/save/chat/',
                dataType:"json",
                data:data,
                contentType:false,
                processData:false,
                success:function(data){
                    $("#pesan_id").text("")
                    
                    // console.log(data)
                },
                error:function(err){
                    console.log(err)
                }
            })
        }
        // console.log($("a#to_user").attr('data-user'))
        
        // loadChat($("p#id_thread").attr('data-thread'))
        setInterval(loadChatAll, 1000)
        
    })
    // setInterval(loadChat($("p#id_thread").attr('data-thread')), 1000)
    // $("div#pesan_id").focusout(function(){ 
    //     console.log($(this).text())
    // })
    $("a#to_user").click(function(){
        createThread($(this).attr('data-user'))
        $(this).data('clicked',true)

        $("p.hidden").remove();
        $("p#username_id").remove();
        
    })

   
    // setInterval(loadChat($("p#id_thread").attr('data-thread')), 1000)
    
   

})
