$(document).ready(function() {

  var $requestBtn = $('.request-payment');

  //call event.preventDefault() once when the Request Payment button is clicked
  $requestBtn.one('click', false);

  $requestBtn.click(function(e) {
    var $amountInput = $(this).prev().prev();

    $amountInput.attr({type: 'number'});

  });

});
