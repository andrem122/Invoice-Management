//File Upload Message
window.addEventListener("load", function(event) {

  var popup = document.getElementsByClassName('popup')[0];

  if (popup !== undefined) {
    popup.style.display = 'block';
  }

  function file_upload_message() {
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

  //pops up or removes modal with 'popup' class when trigger is activated
  function alter_popup(event_type, popup_ele, popup_removable_eles, form) {
    var overlay_ele = document.getElementById('overlay_id');
    if (event_type === 'click') { //for click popups
      document.addEventListener(event_type, function(e){

        //console.log('Classes: ' + e.target.classList.toString() + ' Node Name: ' + e.target.nodeName.toString());

        if(e.target.classList.contains('popup-trigger')) {
          overlay_ele.classList.add('visible');
          popup_ele.classList.add('visible');
        }

        if (e.target.id === popup_removable_eles[0] ||
          e.target.classList.contains(popup_removable_eles[1]) ||
          e.target.classList.contains(popup_removable_eles[2])) {

          overlay_ele.classList.remove('visible');
          popup_ele.classList.remove('visible');
        }


      });
    } else { //for form submit popups
        form.addEventListener('submit', function(e) {
          e.preventDefault();
          form.getElementsByClassName('form-submit-btn')[0].disabled = true;
          overlay_ele.classList.add('visible');
          popup_ele.classList.add('visible'); //show loading popup
          form.submit(); //submit form
        });
    }
  }

  //for send data form popup
  var path = window.location.pathname;
  if (path === '/jobs-admin/' || path === '/payments/' && popup !== null) {
    alter_popup('click', popup, ['overlay_id', 'popup_remove_trigger', 'exit-on-click']);
  }

  if (path === '/add-expense/' || path === '/addjob/' && popup !== null) {
    var form = document.getElementsByClassName('add-form')[0];
    alter_popup('submit', popup, [1, 2, 3], form);
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

    document.addEventListener('click', function(e){
      //console.log('Classes: ' + e.target.classList.toString() + ' Node Name: ' + e.target.nodeName.toString());

      if(e.target.classList.contains('popup-trigger-search') || e.target.classList.contains('search_input_mobile') || e.target.id === 'search_trigger') {
        overlay_ele.classList.add('visible');
        search_popup.classList.add('visible');
        search_popup.focus();
      }

      else if (e.target.id === 'overlay_id') {
        overlay_ele.classList.remove('visible');
        search_popup.classList.remove('visible');
      }
    });
  }

  search_popup();

});
