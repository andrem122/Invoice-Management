//File Upload Message
window.addEventListener("load", function(event) {

  function file_upload_message() {
    //shows uploaded file name in file message element
    document.addEventListener('change', function(e) {
      if(e.target.classList.contains('file_upload')) {
        file_input_ele = e.target;
        file_message_ele = file_input_ele.nextElementSibling;

        file_path_arr = file_input_ele.value.split('\\');
        file_message_ele.innerHTML = file_path_arr[file_path_arr.length - 1];
        file_message_ele.style.display = 'block';
      }
    });
  }

  file_upload_message();

  function alter_popup(event_type, popup_ele, popup_removable_eles, form, switch_popups_on_submit) {
    //pops up or removes modal with 'popup' class when trigger is activated
    var overlay_ele = document.getElementById('overlay_id');
    if (event_type === 'click') { //for click popups
      $(document).on('click touchstart', function(e) {

        //add the 'visible' class to the appropriate elements when the trigger is clicked
        if(e.target.classList.contains('popup-trigger')) {
          overlay_ele.classList.add('visible');
          popup_ele.classList.add('visible');
        }

        //the elements that, when clicked on, remove the popup and overlay
        if (popup_removable_eles !== undefined) {
          if (e.target.id === popup_removable_eles[0] ||
            e.target.classList.contains(popup_removable_eles[1]) ||
            e.target.classList.contains(popup_removable_eles[2])) {

            overlay_ele.classList.remove('visible');
            popup_ele.classList.remove('visible');
          }
        }

        //remove the popup FORM on submit if desired
        if(switch_popups_on_submit === true && popup_ele.nodeName === 'FORM') {

          popup_ele.addEventListener('submit', function() {
            popup_ele.classList.remove('visible');
          });

        }


      });
    } else { //for form submit popups

      if(form !== undefined) {

        form.addEventListener('submit', function(e) {
          e.preventDefault();
          form.getElementsByClassName('form-submit-btn')[0].disabled = true;
          overlay_ele.classList.add('visible');
          popup_ele.classList.add('visible'); //show loading popup
          form.submit(); //submit form
        });

      }


    }
  }

  var path = window.location.pathname;

  //for send data form popup
  var send_data_form_popup = document.getElementById('send-data-form');
  var sending_data_popup = document.getElementById('sending-data-popup');
  if ((path === '/jobs-admin/' || path === '/payments/') && (send_data_form_popup !== null || sending_data_popup !== null)) {
    alter_popup('click', send_data_form_popup, ['overlay_id', 'popup-remove-trigger', 'exit-on-click'], undefined, true);
    alter_popup('submit', sending_data_popup, [1, 2, 3], send_data_form_popup);
  }

  //for the 'sending data' popup that comes up after an expense or job is submitted
  if (path === '/add-expense/' || path === '/addjob/' && sending_data_popup !== null) {
    var add_object_form = document.getElementsByClassName('add-form')[0];
    alter_popup('submit', sending_data_popup, [1, 2, 3], add_object_form);
  }

  if (send_data_form_popup !== undefined) {
    send_data_form_popup.style.display = 'block';
  }

  if(sending_data_popup !== undefined) {
    sending_data_popup.style.display = 'block';
  }

  function search_popup() {

    //elements
    var overlay_ele = document.getElementById('overlay_id');
    var search_popup = document.getElementById('search');

    //if window is greater than or equal to 800px, add 'search_input_mobile' class to search input
    if (window.innerWidth <= 545) {
      search_popup.classList.add('search_input_mobile');
    } else {
      search_popup.classList.remove('search_input_mobile');
    }

    //add toggled class when window resizes above 800px
    window.addEventListener('resize', function() {
      if (window.innerWidth <= 545) {
        //console.log('window width less than 545px!');
        search_popup.classList.add('search_input_mobile');
      } else {
        search_popup.classList.remove('search_input_mobile');
      }
    });

    $(document).on('click touchstart', function(e) {
      //console.log('Classes: ' + e.target.classList.toString() + ' Node Name: ' + e.target.nodeName.toString());

      if(e.target.classList.contains('popup-trigger-search') || e.target.classList.contains('search_input_mobile') || e.target.id === 'search_trigger') {
        overlay_ele.classList.add('visible');
        search_popup.classList.add('visible');
        search_popup.focus();
      }

      else if (e.target.id === 'overlay_id') {
        overlay_ele.classList.remove('visible');
        search_popup.classList.remove('visible');
        search_popup.blur();
      }
      
    });
  }

  search_popup();

});
