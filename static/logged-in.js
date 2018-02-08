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
});
