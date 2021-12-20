var pembinaQuery = `
query{
  allProfile{
    id
    username{
      id
      username
    }
  }
}
`
$(document).ready(function() {
  $.ajax({
    method:'POST',
    url:'/graphql',
    contentType:"application/json",
    data:JSON.stringify({
      query:pembinaQuery,
    }),
    dataType:"json",
    success:function(data){
      users = data['data']['allProfile']
      
      $.each(users, function(user,index) {
        
        $("#id_pembina_admin").append($('<option>', {
          value:index['id'],
          text:index['username']['username']
        }));
      });
    },
    error:function(err){
      console.log(err)
    }
  })
})