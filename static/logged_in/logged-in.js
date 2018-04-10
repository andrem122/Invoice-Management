$(document).ready(function(){
  var $menuToggle = $('#menu-toggle');
  var $wrapper = $('#wrapper');
  var $pageContent = $('#page-content-wrapper');
  var $closeNav = $('.close-nav');

  $menuToggle.click(function(e) {
      e.preventDefault();
      $wrapper.toggleClass("toggled");
  });

  $closeNav.click(function(){
    $wrapper.removeClass('toggled');
  });

  //if window is less than or equal to 800px, remove .toggled class from #wrapper
  if (window.innerWidth <= 800) {
    $wrapper.removeClass('toggled');
  } else {
    $wrapper.addClass('toggled');
  }

  //remove toggled class when window resizes below 800px
  window.addEventListener('resize', function() {
    if (window.innerWidth <= 800) {
      $wrapper.removeClass('toggled');
    } else {
      $wrapper.addClass('toggled');
    }
  });

  //submits a form when button is clicked
  function post_form(class_names) {
    document.addEventListener('click', function(e){
      classes = Array.from(e.target.classList); //convert DOMTicketList to array
      l = class_names.length;
      for (var i = 0; i < l; i++) {
        if(classes.includes(class_names[i])) {
          var form = e.target.parentElement.parentElement;
          form.submit();
        }
      }
    });
  }

  post_form(['v-payment-history-p', 'unapprove-p']);

});
