$(document).ready(function(){
  var $menuToggle = $('#menu-toggle');
  var $wrapper = $('#wrapper');
  var $pageContent = $('#page-content-wrapper');
  var $closeNav = $('.close-nav i');

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

});
