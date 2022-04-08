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
            html = `<p class="hidden" data-thread=${obj[0].pk} data-user=${obj[0].user__pk} data-to-user=${obj[0].to_user__pk} data-username=${obj[0].user__username} id="id_thread"></p>`
            $("a#to_user").attr("data-thread",obj[0].pk)
            if($("#sender").text() !== obj[0].user__username ){
                pesan = `<p class="mt-2" id="username_id">${obj[0].user__username}</p>`
            }else{
                pesan = `<p class="mt-2" id="username_id">${obj[0].to_user__username}</p>`
            }
            
            
            $("#sender").after(html)
            $("p#sender").after(pesan)
            loadChat($("p#id_thread").attr('data-thread'))
        },
        error:function(err){
            console.log(err)
        },
    })
}

function isReadDone(el){
    var data = new FormData()
    data.append("user", el)
    console.log(el)
    $.ajax({
        method:"POST",
        url:'/chat/read/done/',
        data:data,
        dataType:"json",
        contentType:false,
        processData:false,
        success:function(data){
            
        },
        error:function(err){
            console.log(err)
        }
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
                obj.map(data => {
                    
                    html += '<div class="row" style="margin-left:0; margin-right:0"><div class="col-md">';
                    var d = new Date(data.date)
                    var tgl = d.getDate()+'-'+String(d.getMonth()+1).padStart(2,"0")+'-'+d.getFullYear()+' '+d.getHours()+':'+String(d.getMinutes()).padStart(2,"0");
                    if(data.sender__username == username){
                        // console.log(data.sender__username, username)
                        html += '<div class="time sender">'+ tgl +'</div><div class="message sender">'+ data.body+'</div></div></div>'
                    }else{
                        html += '<div class="time">'+ tgl +'</div><div class="message ">'+ data.body+'</div></div></div>'
                    }

                    
                   
                })
                $("#id_pesan").html(html) 
               
            },
            error:function(err){
                console.log(err)
            }
        })
}

function loadRead(){
    for(var i=1;i<ul;i++){
        (function (item) { 
            var to_user = $(`ul#to_users:nth-child(${item}) a`)
            
            var to_user_pk = parseInt(to_user[0].dataset.user)
            var data = new FormData()
            data.append('to_user', to_user[0].dataset.user)

            $.ajax({
                method:"POST",
                url:'/chat/load/read/',
                dataType:"json",
                data:data,
                contentType:false,
                processData:false,
                success:function(data){
                    
                    var datas = data.data
                    // console.log(datas[0].sender_id)
                    // to_user.addClass("new_message")
                    try{
                        
                        // console.log(to_user_pk)
                        if(datas[0].sender_id === to_user_pk){
                            to_user.addClass("new_message")
                        }
                    }catch(err){
                        console.clear()
                    }
                

                    
                },
                error:function(err){
                    console.log(err)
                }
            })
         })(i)
    }
}

function loadChatAll(){
    // var ul = $("ul#to_users").length + 1
    // for(var i=1;i<ul;i++){
    //     console.log(i)
    //     var to_user = $(`ul#to_users:nth-child(${i}) a`)
    //     console.log(to_user[0].innerText)
    // }
    loadChat($("p#id_thread").attr('data-thread'))
    // isReadDone($("p#id_thread").attr('data-thread'))
    
}

function isReadAll(){
    isReadDone($("p#id_thread").attr('data-thread'))
}

var pesan = document.getElementById("pesan_id")

$(document).ready(function(){
    let sender = $("#sender").text()
    let toUser = $("#to_user").text()
    setInterval( loadRead, 1000)
    loadRead()
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

        // var data = new FormData()
        // data.append("user",$("p#id_thread").attr('data-to-user'))

        // $.ajax({
        //     method:"POST",
        //     url:'/chat/read/done/',
        //     data:data,
        //     dataType:"json",
        //     contentType:false,
        //     processData:false,
        //     success:function(data){
                
        //     },
        //     error:function(err){
        //         console.log(err)
        //     }
        // })
        
    })

    $("a#to_user").click(function(){
        
        createThread($(this).attr('data-user'))
        $(this).data('clicked',true)

        $("p.hidden").remove();
        $("p#username_id").remove();

        setInterval(loadChatAll, 1000)
        if($(this).hasClass("new_message")){
            $(this).removeClass("new_message")
            
            isReadDone($(this).attr("data-user"))
        }
        
    })

})
