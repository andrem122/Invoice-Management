window.addEventListener('DOMContentLoaded', function() {
  // Google Autocomplete
  var autocomplete = initialize('id_address'); // function initialize is from a seperate file called 'google_places.js'

  // Get elements we need and cache them for use later on
  var form = document.getElementById('add-company-form');
  var city_input = document.getElementById('id_city');
  var state_input = document.getElementById('id_state');
  var zip_input = document.getElementById('id_zip');
  var select_all_days_checkbox = document.getElementById('select_all_days_of_the_week_enabled');
  var select_all_hours_checkbox = document.getElementById('select_all_hours_of_the_day_enabled');

  // Get elements needed for slider to work
  var next_button = document.getElementById('id_next_button');
  var back_button = document.getElementById('id_back_button');
  var slides = document.getElementsByClassName('form-slider-slide-container');
  var slides_length = slides.length;
  var slide_index = 0;

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

  function hideSlidesOnLoad() {
    // Make only the first slide visible and hide the rest
    for (var i = 0; i < slides_length; i++) {
      slides[i].style.display = 'none';
    }

    // Show first slide
    slides[0].style.display = 'block';
  }

  hideSlidesOnLoad();

  function toggle_back_button() {
    // Hides the back button if the slider is on the first slide
    // and shows it if we are on the second slide

    if (slide_index >= 1) {
      back_button.style.display = 'block';
      next_button.style.marginBottom = '30px';
    } else {
      back_button.style.display = 'none';
      next_button.style.marginBottom = '0';
    }
  }

  function toggle_next_button_text() {
    // Toggles the text of the next button between
    // 'Get Free Software' and 'Next' depending on the slide index

    if (slide_index == slides_length - 1) {
      next_button.innerHTML = 'Get Free Software!';
    } else {
      next_button.innerHTML = 'Next';
    }

  }

  function next_button_clicked(event) {
    // Shows the appropriate slide when the next button is clicked

    // Hide current slide
    var currentSlide = slides[slide_index];
    currentSlide.classList.remove('animated', 'bounceInRight');
    currentSlide.classList.add('animated', 'bounceOutLeft');
    currentSlide.style.display = 'none';

    slide_index += 1; // Increase slide_index by one
    if(slide_index >= slides_length) {
      // Submits the form if on the last slide and next button is clicked
      slide_index = 0;
      form.submit();
      return;
    }

    // Toggle back button if needed
    toggle_back_button();
    toggle_next_button_text();

    // Show next slide
    var nextSlide = slides[slide_index];
    nextSlide.style.display = 'block';
    nextSlide.classList.remove('animated', 'bounceInLeft', 'bounceOutLeft', 'bounceOutRight', 'bounceInRight');
    nextSlide.classList.add('animated', 'bounceInRight');

  }

  function back_button_clicked(event) {
    // Shows the appropriate slide when the back button is clicked

    // Hide current slide
    var currentSlide = slides[slide_index];
    currentSlide.classList.remove('animated', 'bounceInLeft', 'bounceOutLeft', 'bounceOutRight', 'bounceInRight');
    currentSlide.classList.add('animated', 'bounceOutRight');
    currentSlide.style.display = 'none';

    slide_index -= 1; // Increase slide_index by one
    // Check if index is in range of our slides list
    if(slide_index < 0) {
      // reset to last slide
      slide_index = slides_length - 1;
    }

    // Toggle back button if needed
    toggle_back_button();
    toggle_next_button_text();

    // Show next slide
    var nextSlide = slides[slide_index];
    nextSlide.style.display = 'block';
    nextSlide.classList.remove('animated', 'bounceInLeft', 'bounceOutLeft', 'bounceOutRight', 'bounceInRight');
    nextSlide.classList.add('animated', 'bounceInLeft');

  }

  // Slider events
  next_button.addEventListener('click',  next_button_clicked);
  back_button.addEventListener('click',  back_button_clicked);

  // Google places events
  google.maps.event.addListener(autocomplete, 'place_changed', fill_in_address);

  // Checkbox events
  select_all_days_checkbox.addEventListener('click', select_all);
  select_all_hours_checkbox.addEventListener('click', select_all);

});
