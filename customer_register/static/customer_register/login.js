document.addEventListener('DOMContentLoaded', function(e){

  var phone_number_input = document.getElementById('id_phone_number');
  phone_number_input.addEventListener('input', function(e) {
    //formats phone numbers to (XXX) XXX-XXXX
    var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
    e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');

  });

  document.getElementById('register-form').addEventListener('submit', function(e) {
    e.preventDefault();
    //format phone number from (XXX) XXX-XXXX to +1XXXXXXXXXX
    var phone_number_as_e164 = "+1" + phone_number_input.value.replace(/["'()-\s]/g, "");
    phone_number_input.value = phone_number_as_e164;
    this.submit();
  });

});
