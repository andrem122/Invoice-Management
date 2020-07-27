window.addEventListener('DOMContentLoaded', function() {
  // Google Autocomplete
  var autocomplete = initialize('id_address'); // function initialize is from a seperate file called 'google_places.js'

  // Get elements we need and cache them for use later on
  var form = document.getElementById('add-company-form');
  var city_input = document.getElementById('id_city');
  var state_input = document.getElementById('id_state');
  var zip_input = document.getElementById('id_zip');
  var select_all_options_checkboxes = document.getElementsByClassName('select_all_options_checkbox');

  function fill_in_address() {
    // Fills in the city, state, and zip fields when the user
    // selects an address from the autocomplete drop down

    var place = autocomplete.getPlace();
    var city, state, zip; // Initialize
    city = state = zip = '';

    var l = place.address_components.length;
    for (var i = 0; i < l; i++) {
      var addressType = place.address_components[i].types[0];

      // Get the city, state, and zip from the google place object
      if(addressType == 'locality') { // City
        city = place.address_components[i].long_name;
      }

      else if(addressType == 'administrative_area_level_1') { // State
        state = place.address_components[i].short_name;
      }

      else if(addressType == 'postal_code') { // Zip code
        zip = place.address_components[i].long_name;
      }

    }

    // Set the values for the input fields
    city_input.value = city;
    state_input.value = state;
    zip_input.value = zip;
  }

  function select_all() {
    // Selects all the check items when the 'Select All' option is selected
    var ul_parent = this.parentElement.parentElement.parentElement; // Get the parent unordered list containing all the options

    // If the 'Select All' checkbox is selected already, check all the checkboxes
    // else uncheck all the checkboxes
    var checked = false;
    if (this.checked === true) {
      checked = true;
    } else {
      checked = false;
    }

    // Loop through the option in the unordered list
    var l = ul_parent.children.length;
    for (var i = 1; i < l; i++) {
      checkbox = ul_parent.children[i].children[0].children[0];
      checkbox.checked = checked;
    }
  }

  // Google places events
  google.maps.event.addListener(autocomplete, 'place_changed', fill_in_address);

  // Checkbox events
  var l = select_all_options_checkboxes.length;
  for (var i = 0; i < l; i++) {
    select_all_options_checkboxes[i].addEventListener('click', select_all);
  }

});
