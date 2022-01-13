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
                console.log(data)
            },
            error:function(err){
                console.log(err)
            }
        })
        console.log($(this).text())
    })
})