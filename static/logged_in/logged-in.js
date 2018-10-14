//loader and intro js
window.addEventListener("load", function(event) {
  var wrapper = document.getElementById('wrapper');
  var loader = document.getElementById('loader');
  wrapper.style.display = 'block';
  loader.style.display = 'none';

  var send_data_form = document.getElementById('send-data-form');
  var overlay = document.getElementById('overlay_id');
  if(send_data_form !== null) {
    send_data_form.style.display = 'block';
  }

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

  //submits a form when button is clicked
  function post_form(class_names) {
    document.addEventListener('click', function(e){
      var classes = Array.from(e.target.classList); //convert DOMTicketList to array
      l = class_names.length;
      var clicked = false; //prevent multiple submissions of forms
      for (var i = 0; i < l; i++) {
        if(classes.includes(class_names[i]) && clicked === false) {
          clicked = true;
          var form = e.target.parentElement.parentElement;
          form.submit();
        }
      }
    });
  }

  post_form(['submit-p']);

  function submit_upload_form() {
    document.addEventListener('change', function(e){
      classes = e.target.classList;
      if(classes.contains('document_link_upload') || classes.contains('document_link_upload-m')) {
        //submit upload form when file is uploaded
        console.log(e.target.id);
        e.target.form.submit();
      }

    });
  }

  submit_upload_form();

  //submits forms and shows hidden inputs when button is clicked
  function post_form_with_file_input(class_names, type) {
    var clicks = 0;
    document.addEventListener('click', function(e){

      var classes = Array.from(e.target.classList); //convert DOMTicketList to array
      l = class_names.length;

      for(var i = 0; i < l; i++) {
        if(classes.includes(class_names[i])) {
          clicks += 1;
          var form = e.target.parentElement.parentElement;
          var target_input = form.children[1];
          if(clicks === 1) {
            e.preventDefault();
            target_input.setAttribute('type', type);
          } else {
            if(target_input.value !== '' && target_input.value !== '0.0') {
              form.submit();
            }
          }
        }
      }
    });
  }

  post_form_with_file_input(['upload-document-p'], 'file');
  post_form_with_file_input(['request-payment-p'], 'number');

  //pop up send data form when button is clicked
  document.addEventListener('click', function(e){

    if(e.target.id === 'send-data-btn') {
      overlay.classList.add('visible');
      send_data_form.classList.add('visible');
    }

    else if (e.target.id === 'overlay_id' || e.target.nodeName === 'path'|| e.target.id === 'send-data-exit') {
      overlay.classList.remove('visible');
      send_data_form.classList.remove('visible');
    }
  });

  //activate intro js if it is a new user
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

  /*Scroll to top when arrow up clicked BEGIN*/
  $scroll_btn = $('#scroll');
  $('body').scroll(function(){
    if ($(this).scrollTop() > 2) {
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

});
