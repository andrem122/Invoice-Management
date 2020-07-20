window.addEventListener('DOMContentLoaded', function() {

  function check_if_exists(selector, function_to_run) {
    // Waits until an element exists in the DOM
    var checkExist = setInterval(
      function() {
       if ($(selector).length) {
          clearInterval(checkExist);
          function_to_run();
       }
      }, 100);
  }

  function get_parent(el, parent_selector /* optional */) {

    // If no parent_selector defined will bubble up all the way to *document*
    if (parent_selector === undefined) {
        parent_selector = document;
    }

    var p = el.parentElement;

    //determine if it's a class or id
    parent_selector_type = parent_selector[0];
    var o = null;

    if(parent_selector_type === '.') { //class
      parent_selector = parent_selector.split('.')[1];
      while(!p.classList.contains(parent_selector)) {
          o = p;
          p = o.parentElement;
      }
    }

    else if(parent_selector_type === '#') { //id
      parent_selector = parent_selector.split('#')[1];
      while (p.id !== parent_selector) {
          o = p;
          p = o.parentElement;
      }
    }

    return p;
  }

  // Cache the DOM
  var overlay = document.getElementById('overlay');

  // Action popup
  var action_popup = document.getElementById('actions-popup');
  var remove_popup_buttons = document.getElementsByClassName('remove-popup-btn');

  // Delete popup
  var confirm_action_buttons = document.getElementsByClassName('confirm_action_button');
  var delete_popup = document.getElementById('delete-popup');

  var all_popups = document.getElementsByClassName('popup');

  function show_popup(popup_element, actions_button, append_to_href_of_popup_options) {

    // Show the popup and overlay
    if (popup_element.style.visibility == 'visible') {

      overlay.style.opacity = 0;
      overlay.style.visibility = 'hidden';

      popup_element.style.opacity = 0;
      popup_element.style.visibility = 'hidden';
    } else {

      overlay.style.opacity = 1;
      overlay.style.visibility = 'visible';

      popup_element.style.opacity = 1;
      popup_element.style.visibility = 'visible';
    }

    // If we want to append a GET parameter to the href of the popup action anchor tags
    if (append_to_href_of_popup_options === true) {
      // Add company parameter to each href attribute for each action option
      var object_id = actions_button.getAttribute('data-object-id');
      var popup_options = popup_element.getElementsByClassName('action_option');

      var popup_options_length = popup_options.length;
      for (var i = 0; i < popup_options_length; i++) {
        // Get the href string
        var href = popup_options[i].getAttribute('href');
        // If the href already has parameter 'c', then dont add it to the end of the href
        if (!href.includes('?')) {
          href += '?c=' + object_id;
        } else {

          // Split the href string, grab the first part before the '=' sign and add the new company id string
          var split_href = href.split('=');
          href = split_href[0] + '=' + object_id;
        }

        popup_options[i].href = href;
      }
    }

  }

  function remove_popup() {
    // Removes the popup and overlay from view
    overlay.style.opacity = 0;
    overlay.style.visibility = 'hidden';

    // Remove ALL popups from view
    var all_popups_length = all_popups.length;
    for (var i = 0; i < all_popups_length; i++) {
      all_popups[i].style.opacity = 0;
      all_popups[i].style.visibility = 'hidden';
    }
  }

  // Check if the font awesome element exists before we add a class to its children
  check_if_exists('svg.fa-ellipsis-v', function() {
    // Adds the trigger class to nested elements in parent elements
    var parent_elements = document.getElementsByClassName('fa-ellipsis-v');

    var l = parent_elements.length;
    for (var i = 0; i < l; i++) {

      // Loop through children and add the trigger class to each one
      var children_length = parent_elements[i].children.length;
      var children = parent_elements[i].children;
      for (var j = 0; j < children_length; j++) {
        children[j].classList.add('actions-trigger');
      }

    }
  });

  // Actions popup triggers
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('actions-trigger')) {
      // Set the actions_button to get the data-object-id
      actions_button = e.target;
      if(actions_button.nodeName !== 'BUTTON') { // if the actions_button button is clicked on, pass it as the argument else get the actions_button
        actions_button = get_parent(e.target, '.actions-btn');
      }
      show_popup(action_popup, actions_button, true);
    }
  });

  // Delete popup triggers
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('delete-trigger')) {
      // Set the actions_button to get the data-object-id
      show_popup(delete_popup, e.target, true);
    }
  });

  // Remove overlay and popup on click of overlay
  overlay.addEventListener('click', remove_popup);

  // 'X' Cancel buttons on popups
  var remove_popup_buttons_length = remove_popup_buttons.length;
  for (var k = 0; k < remove_popup_buttons_length; k++) {
    remove_popup_buttons[k].addEventListener('click', remove_popup);
  }

  // Cancel button in delete popup
  if (confirm_action_buttons !== null) {
    var confirm_action_buttons_length = confirm_action_buttons.length;
    for (var j = 0; j < confirm_action_buttons_length; j++) {
      confirm_action_buttons[j].addEventListener('click', remove_popup);
    }
  }

});
