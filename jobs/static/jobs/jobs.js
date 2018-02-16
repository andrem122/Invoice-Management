$(document).ready(function() {

  var $requestBtn = $('.request-payment');
  var $messages = $('ul.messages');
  var $form = $('.request-payment-form');

  //call event.preventDefault() once when the Request Payment button is clicked
  $requestBtn.one('click', false);

  $requestBtn.click(function(e) {
    var $amountInput = $(this).prev().prev();

    $amountInput.attr({type: 'number'});

  });

  $form.submit(function(){
    $(this).find('ul.messages').css('display', 'block');
    console.log('form submitted');
  });

});
