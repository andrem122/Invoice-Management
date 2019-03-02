document.addEventListener('DOMContentLoaded', function(e){

  document.getElementById('id_phone_number').addEventListener('input', function (e) {
    //formats phone numbers to (XXX) XXX - XXXX
    var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
    e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');

  });

});
