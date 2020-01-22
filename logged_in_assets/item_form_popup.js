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

  function item_options_popup(element_to_popup_class, trigger_button_classes, overlay_element, parent_to_fetch_class) {
    /**
   * Pops up the item options and edit item forms for an object into a user's view for mobile devices.
   * @param {string} element_to_popup_class The class of the element to popup into view.
   * @param {array} trigger_button_classes The classes of the elements that will be clicked on or touched.
   * @param {object} overlay_element The overlay (background) element to popup into view.
   * @return {null} Nothing returned.
   */

    // Declare local variables to be used throughout the whole function
    var popup_forms, popup_element = null;

    // For mobile item popups
    $(document).on('click touchend', function(e) {

      // Loop through trigger_button_classes
      var l = trigger_button_classes.length;
      for(var i = 0; i < l; i++) {

        if(e.target.classList.contains(trigger_button_classes[i])) {
          // Get the parent element containing the mobile options popup list
          popup_forms = get_parent(e.target, parent_to_fetch_class).previousElementSibling; //gets .popup-forms

          // Get the element that will popup
          popup_element = popup_forms.getElementsByClassName(element_to_popup_class)[0];

          // Make element and overlay visible
          if(!popup_element.classList.contains('visible') || !overlay_element.classList.contains('visible') && popup_element !== null) {
            popup_element.classList.add('visible');
            overlay_element.classList.add('visible');
            popup_forms.style.display = 'block'; // .popup-forms is set to display: none by default
            popup_forms.classList.add('flex-container');
          }

        } else if // Handles the exit out of the popups
        (
          e.target.classList.contains('overlay') ||
          e.target.classList.contains('exit-on-click') ||
          e.target.classList.contains('popup-remove-trigger')
        ) {
          overlay_element.classList.remove('visible');

          // Only manipulate the popup_forms and popup_element if they are defined and not null
          if(popup_forms !== null && popup_forms !== undefined) {
            popup_element.classList.remove('visible');
            popup_forms.style.display = 'none';
            popup_forms.classList.remove('flex-container');
          }

        }

      }

    });

  }

  function trigger_within_popup(element_to_popup_class, trigger_button_classes, overlay_element, parent_to_fetch_class) {
    /**
   * Pops up a popup element within a popup element and removes previous popup element from view.
   * @param {string} element_to_popup_class The class of the element to popup into view.
   * @param {array} trigger_button_classes The classes of the elements that will be clicked on or touched.
   * @param {object} overlay_element The overlay (background) element to popup into view.
   * @param {string} parent_to_fetch_class The class of element containing the popup forms.
   * @return {null} Nothing returned.
   */

   // Declare local variables to be used throughout the whole function
   var popup_forms, popup_element = null;

   // For mobile item popups
   $(document).on('click touchend', function(e) {
     // Loop through trigger_button_classes
     var l = trigger_button_classes.length;
     for(var i = 0; i < l; i++) {

       if(e.target.classList.contains(trigger_button_classes[i])) {
         // Get the parent element containing the mobile options popup list
         popup_forms = get_parent(e.target, parent_to_fetch_class);

         // Get the element that will popup
         popup_element = popup_forms.getElementsByClassName(element_to_popup_class)[0];

         // Make element and overlay visible and remove previous popup from view
         if(!popup_element.classList.contains('visible') || !overlay_element.classList.contains('visible') && popup_element !== null) {
           popup_element.classList.add('visible');
           popup_element.nextElementSibling.classList.remove('visible'); // gets popup element to remove and removes 'visible' class
           overlay_element.classList.add('visible');
           popup_forms.style.display = 'block'; // .popup-forms is set to display: none by default
           popup_forms.classList.add('flex-container');
         }

       } else if // Handles the exit out of the popups
       (
         e.target.classList.contains('overlay') ||
         e.target.classList.contains('exit-on-click') ||
         e.target.classList.contains('popup-remove-trigger')
       ) {
         overlay_element.classList.remove('visible');

         // Only manipulate the popup_forms and popup_element if they are defined and not null
         if(popup_forms !== null && popup_forms !== undefined) {
           popup_element.classList.remove('visible');
           popup_forms.style.display = 'none';
           popup_forms.classList.remove('flex-container');
         }

       }

     }

   });
  }

  var overlay = document.getElementById('overlay_id');
  trigger_within_popup('edit-item-form', ['edit-item-option-m'], overlay, '.popup-forms');
  item_options_popup('mobile-option-icons', ['item-options-toggle-mobile-btn'], overlay, '.item-container');
  item_options_popup('edit-item-form', ['edit-job-option', 'edit-expense-option', 'edit-project-option'], overlay, '.item-container');

});
