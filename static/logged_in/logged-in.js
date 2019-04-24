//loader and intro js
window.addEventListener("load", function(event) {
  document.body.style.visibility='visible';
  var wrapper = document.getElementById('wrapper');
  var loader = document.getElementById('loader');
  wrapper.style.display = 'block';
  loader.style.display = 'none';

  var $menu_toggle = $('#menu-toggle');
  var $wrapper = $('#wrapper');
  var $close_nav = $('.close-nav');

  $menu_toggle.click(function(e) {
      e.preventDefault();
      $wrapper.toggleClass("toggled");
  });

  $close_nav.click(function(){
    $wrapper.removeClass('toggled');
  });

  //if window is greater than or equal to 800px, add toggled class to #wrapper
  if (window.innerWidth >= 800) {
    $wrapper.addClass('toggled');
  } else {
    $wrapper.removeClass('toggled');
  }

  //add toggled class when window resizes above 800px
  window.addEventListener('resize', function() {
    if (window.innerWidth >= 800) {
      $wrapper.addClass('toggled');
    } else {
      $wrapper.removeClass('toggled');
    }
  });

  /* Scroll to top when arrow up clicked */
  $scroll_btn = $('#scroll');
  $('window').scroll(function(){
    if ($(this).scrollTop() > 2) {
      console.log('Scroll button visible');
      $scroll_btn.removeClass('hidden');
      $scroll_btn.addClass('visible');
    } else {
      $scroll_btn.removeClass('visible');
      $scroll_btn.addClass('hidden');
    }
  });

  $('#scroll').click(function(){
    $("html, body").animate({ scrollTop: 0 }, 600);
    return false;
  });

  function upload_document_form_on_change() {
    //submits uploaded document as soon as the user uploads the document into the input element
    document.addEventListener('change', function(e){
      if(e.target.classList.contains('paid_link_upload') || e.target.classList.contains('paid_link_upload_m')) {
        //submit upload form when file is uploaded
        e.target.form.submit();
      }

    });
  }

  upload_document_form_on_change();

  //activate intro js if it is a new user
  /*
  if (document.documentURI.indexOf('new_user=True') !== -1) {
    //disable add job button
    var addJobBtn = document.getElementById('add-job');
    var href = addJobBtn.href;
    addJobBtn.setAttribute('href', '#');

    //get request payment button for caching
    var requestBtn = document.getElementById('step-2');

    var intro = introJs();
    intro.oncomplete(function(){
      var jobExample = document.getElementsByClassName('job-container')[0];
      jobExample.parentElement.removeChild(jobExample);
      addJobBtn.setAttribute('href', href);
    });

    //scroll request button into view on step 2
    intro.onchange(function(targetElement) {
      console.log(targetElement.id);
      switch (targetElement.id) {
        case 'step-2':
          requestBtn.scrollIntoView();
          break;
      }
    });

    intro.setOptions(
      {'exitOnOverlayClick': false,
      'showProgress': true,
      'showBullets': false,
      'hidePrev': true,
      'hideNext': true,
      'disableInteraction': true,
      }).start();
  }
  */

});
