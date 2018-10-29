//File Upload Message
window.addEventListener("load", function(event) {

  var file_message_ele = document.getElementById('file-input-message');
  var file_input_ele = document.getElementById('id_document_link');

  var popup = document.getElementsByClassName('popup')[0];
  var overlay = document.getElementById('overlay_id');
  var form = document.getElementsByClassName('add-form')[0];

  if (popup !== null) {
    popup.style.display = 'block';
  }

  function file_upload_message(file_message_ele, file_input_ele) {
    file_input_ele.addEventListener('change', function() {
      file_path_arr = file_input_ele.value.split('\\');
      file_message_ele.innerHTML = file_path_arr[file_path_arr.length - 1];
      file_message_ele.style.display = 'block';
    });
  }

  if (file_input_ele !== null && file_message_ele !== null) {
    file_upload_message(file_message_ele, file_input_ele);
  }

  //pops up or removes modal with 'popup' class when trigger is activated
  function alter_popup(event_type, popup_ele, overlay_ele, popup_removable_eles, form) {

    if (event_type === 'click') {
      document.addEventListener(event_type, function(e){

        if(e.target.classList.contains('popup-trigger')) {
          overlay_ele.classList.add('visible');
          popup_ele.classList.add('visible');
        }

        if (e.target.id === popup_removable_eles[0] || e.target.nodeName === popup_removable_eles[1] || e.target.classList.contains(popup_removable_eles[2])) {
          overlay_ele.classList.remove('visible');
          popup_ele.classList.remove('visible');
        }


      });
    } else {
        form.addEventListener('submit', function(e) {
          e.preventDefault();
          form.getElementsByClassName('form-submit-btn')[0].disabled = true;
          overlay_ele.classList.add('visible');
          popup_ele.classList.add('visible'); //show popup
          form.submit(); //submit form
        });
    }
  }

  //for send data form popup
  var path = window.location.pathname;
  if (path === '/jobs-admin/' || path === '/payments/') {
    alter_popup('click', popup, overlay, ['overlay_id', 'path', 'popup_remove_trigger']);
  }

  if (path === '/add-expense/' || path === '/addjob/') {
    alter_popup('submit', popup, overlay, [1, 2, 3], form);
  }

});
