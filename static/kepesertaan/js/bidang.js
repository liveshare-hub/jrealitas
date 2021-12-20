
function chainSelect(current, target){
    var value1 = $(current).on('change', function(){
      if($(this).find(':selected').val() != ''){
        $(target).removeAttr('disabled');
        var value = $(this).find(':selected').text();
      }else{
        $(target).prop('disabled', 'disabled').val(null);
      }
    return value;
    });
    return value1;
  }
  bidang = chainSelect('select#bidang', '#makeselect');
  //color = chainSelect('select#color', '#qty');
  jabatan = chainSelect('select#makeselect', '#daftar_pembina_btn');
  
 console.log(bidang)
 console.log(jabatan)  
  