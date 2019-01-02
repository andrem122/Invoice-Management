document.addEventListener('DOMContentLoaded', function(e){

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
      while (!p.classList.contains(parent_selector)) {
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

  function item_form_popup(trigger_classes, element_to_popup_class, overlay) {
    var popup_forms, form = null;
    document.addEventListener('click', function(e) {
      var l = trigger_classes.length;
      for(var i = 0; i < l; i++) {
        if(e.target.classList.contains(trigger_classes[i])) {

          //if the parent of the target element is NOT .popup-forms, get it
          console.log(e.target);
          if (e.target.classList.contains('edit-item-popup-mobile')) {
            popup_forms = get_parent(e.target, '.popup-forms');
          } else {
            popup_forms = get_parent(e.target, '.item-container').previousElementSibling; //gets .popup-forms
          }

          popup_forms.classList.add('flex-container'); //centers the popup

          //get the popup and make it visible
          popup_element = popup_forms.getElementsByClassName(element_to_popup_class)[0];
          console.log("Popup Element: " + popup_element.className);
          popup_element.classList.add('visible');
          overlay.classList.add('visible');

          popup_element.scrollIntoView(true);

          if(e.target.classList.contains('trigger-within-popup')) {

            //remove the class 'visible' from all other popups except the wanted popup
            console.log('Detected a trigger element within a popup element. Class name of wanted popup is ' + popup_element.className + '.');
            var len = popup_forms.childElementCount;
            var wanted_popup_class = popup_element.className;

            for(var j = 0; j < len; j++) {

              var popup = popup_forms.children[j];
              console.log(popup.className);
              if(popup.className !== wanted_popup_class) {

                popup.classList.remove('visible');
                console.log("Popup " + popup.className + " is no longer visible.");

              }

            }

          }

        } else if (e.target.classList.contains('overlay') || e.target.classList.contains('popup_remove_trigger') ||
                   e.target.classList.contains('exit-on-click')
                 ) { //remove all forms from view
            console.log("All popups will be removed from visibility.");
            if(popup_forms !== null && popup_element !== null) {

              popup_forms.classList.remove('flex-container');
              popup_element.classList.remove('visible');
              overlay.classList.remove('visible');

            }

        }

      }

    });

  }
  var overlay = document.getElementById('overlay_id');
  item_form_popup(['edit-item-popup'], 'edit-job-form', overlay);
  item_form_popup(['item-options-toggle-mobile-btn'], 'mobile-option-icons', overlay);

  if(document.location.pathname === '/jobs/') {
    item_form_popup(['request-money-popup', 'popup'], 'request_payment_form', overlay);
  }

});
