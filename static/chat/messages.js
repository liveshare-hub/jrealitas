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
            $("div[id*=name_contact]").remove();
            $("#id_thread").remove();
            var obj = data.data
            
            html = `<div data-thread=${obj[0].pk} data-user=${obj[0].user__pk} data-to-user=${obj[0].to_user__pk} id="id_thread" hidden></div>`
            html2 = `<div class="name_contact" id="name_contact">${obj[0].to_user__username}</div><div class="seen" id="name_contact">Today at 12:56</div>`
            $("#sender").after(html2)
            $("#sender").after(html)
            loadChat($("div#id_thread").attr('data-thread'))
            
            $("#pesan_id").attr('disabled',false)
        },
        error:function(err){
            console.log(err)
        },
    })
}

function loadChat(el){
    let from = $("div#id_thread").attr('data-user')
    let username = $("#sender").attr('data-username')
    let recipent = $("div#id_thread").attr('data-to-user')
    
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
                
                const obj = data.data
                
                let html = '';
                var size = obj.length;
                for (let count = 0; count < size; count++) {
                
                    // html += '<div class="row" style="margin-left:0; margin-right:0"><div class="col-md">';

                    var d = new Date(obj[count].date)
                    var tgl = d.getDate()+'-'+String(d.getMonth()+1).padStart(2,"0")+'-'+d.getFullYear()+' '+d.getHours()+':'+String(d.getMinutes()).padStart(2,"0")
                    
                    if (obj[count].user__username === username) {
                        console.log(obj[count].user__username)
                        html += '<div class="time sender">'+ tgl +'</div><div class="message sender">'+ obj[count].body+'</div>'
            //             html += '<div class="row"><div align="right" class="col-md"><span class = "text-muted"><small><b>' + tgl + '</b></small></span></div></div>';
            //             html += '<div class="row justify-content-end"><div align="right" class="col-md-8 alert alert-success">';
            //             html += '<div style="font-size:14px;">' + obj[count].fields.body + '</div></div></div></div></div>'; 
                    }
                    else{
                        console.log(obj[count].user__username)
                        html += '<div class="time">'+ tgl +'</div><div class="message '+obj[count].recipent__username +'">'+ obj[count].body+'</div>'
                    }
            //         else {
            //             html += '<div class="row"><div align="left" class="col-md"><span class = "text-muted"><small><b>' + tgl + '</b></small></span></div></div>';
            //             html += '<div class="row"><div align="left" class="col-md-8  alert alert-secondary">';
            //             html += '<div style="font-size:14px;">' + obj[count].fields.body + '</div></div></div></div></div>';
            //         }
                  
               }
               $("#chat").html(html)
            },
            error:function(err){
                console.log(err)
            }
        })
}

function loadChatAll(){
    loadChat($("div#id_thread").attr('data-thread'))
}

var pesan = document.getElementById("pesan_id")

$(document).ready(function(){
    let sender = $("#sender").text()
    let toUser = $("#to_user").text()
    $("#kirim_pesan").attr('disabled',true)
    $("#pesan_id").attr('disabled',true)
    $("#pesan_id").on("focusout",function(){
        if($(this).text !== ""){
            $("#kirim_pesan").attr('disabled',false)
        }else{
            $("#kirim_pesan").attr('disabled',true)
        }
    })
    $("#kirim_pesan").click(function(){
        console.log($("#id_thread").attr('data-thread'))
        if(pesan.value !== ""){
            
            $(this).attr('disabled',false)
            var data = new FormData()
            data.append("pesan",$("#pesan_id").val())
            data.append("thread_id",$("div#id_thread").attr('data-thread'))
            // data.append("to_user",$("p#id_thread").attr('data-to-user'))
            data.append("to_user",$("div#to_user").attr('data-user'))
    
            $.ajax({
                method:'POST',
                url:'/chat/save/chat/',
                dataType:"json",
                data:data,
                contentType:false,
                processData:false,
                success:function(data){
                    $("#pesan_id").val("")
                    
                    // console.log(data)
                },
                error:function(err){
                    console.log(err)
                }
            })
        }
       
        setInterval(loadChatAll, 1000)
        
    })
    
    $("div#to_user").click(function(){
        createThread($(this).attr('data-user'))
        $(this).data('clicked',true)

        $("div.hidden").remove();
        
    })


    
   

})
