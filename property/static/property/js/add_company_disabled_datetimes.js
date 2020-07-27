window.addEventListener('DOMContentLoaded', function() {

  function show_slide_with_index(index) {
    // Hides the current slide and show the slide with the given index

    // Hide the current slide
    var currentSlide = slides[slide_index];
    currentSlide.classList.remove('animated', 'bounceInLeft', 'bounceOutLeft', 'bounceOutRight', 'bounceInRight');
    currentSlide.classList.add('animated', 'bounceOutRight');
    currentSlide.style.display = 'none';

    slide_index = index;

    // Show slide by index
    // Toggle next button text if needed
    toggle_next_button_text();

    // Show next slide
    var nextSlide = slides[slide_index];
    nextSlide.style.display = 'block';
    nextSlide.classList.remove('animated', 'bounceInLeft', 'bounceOutLeft', 'bounceOutRight', 'bounceInRight');
    nextSlide.classList.add('animated', 'bounceInRight');

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

  function uncheck_checkboxes() {
    // Unchecks all checkboxes

    // Loop through the option in the unordered list
    var ul_parents_of_checkboxes_length = ul_parents_of_checkboxes.length;
    for (var i = 0; i < ul_parents_of_checkboxes_length; i++) {
      var l = ul_parents_of_checkboxes[i].children.length;
      for (var j = 1; j < l; j++) {
        checkbox = ul_parents_of_checkboxes[i].children[j].children[0].children[0];
        checkbox.checked = false;
      }
    }
  }

  function toggle_next_button_text() {
    // Toggles the text of the next button between
    // 'Get Free Software' and 'Next' depending on the slide index

    if (slide_index === slides_length - 1 || slide_index === 2) {
      next_button.innerHTML = 'Add Disabled Time';
    } else {
      next_button.innerHTML = 'Next';
    }

  }

  function next_button_clicked(event) {
    // Shows the appropriate slide when the next button is clicked

    // Hide current slide
    var currentSlide = slides[slide_index];
    if(slide_index !== 2 && slide_index !== 3) { // if on the 'submit' form slides, do not hide the current slide when the button is clicked
      currentSlide.classList.remove('animated', 'bounceInRight');
      currentSlide.classList.add('animated', 'bounceOutLeft');
      currentSlide.style.display = 'none';
    }

    slide_index += 1; // Increase slide_index by one
    if(slide_index >= slides_length || slide_index === 3) {
      var form = document.getElementById('add_company_disabled_datetimes');

      // Reset slide index to appropriate slide after POST request
      if (slide_index === 3) {
        slide_index = 2;
      } else if(slide_index === 4) {
        slide_index = 3;
      }

      ajax_create(document.location.href, form, alert_message_element, view_href).done(function(jqXHR) {
        // Clear the selected options on the form
        uncheck_checkboxes();
      }).fail(function(jqXHR) {
        // Get the error slide index from the error json object so we can show the sldie
        show_slide_with_index(jqXHR.responseJSON.slide_index);
      });

      window.scroll({
        top: 0,
        left: 0,
        behavior: 'smooth'
      }); // Scroll to the top of the page so the user can see the alert message

      return;
    }

    console.log(slide_index);

    // Toggle next button text if needed
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
    console.log('BACK BUTTON CLICKED' + slide_index);
    var currentSlide = slides[slide_index];
    currentSlide.classList.remove('animated', 'bounceInLeft', 'bounceOutLeft', 'bounceOutRight', 'bounceInRight');
    currentSlide.classList.add('animated', 'bounceOutRight');
    currentSlide.style.display = 'none';

    // If on the add disabled datetime slide, hide the button container and go to the first slide
    if(slide_index === 3) {
      slider_action_buttons_container.style.display = 'none';
      slide_index = 0;
    } else if(slide_index === 1) { // If on the first slide (select a disabled day option), hide the button container
      slider_action_buttons_container.style.display = 'none';
      slide_index -= 1; // Decrease slide_index by one
    } else {
      slide_index -= 1;
    }

    // If going back to the first slide, hide the alert_message_element
    if(slide_index === 0) {
      alert_message_element.style.display = 'none';
    }

    // Toggle next button text if needed
    toggle_next_button_text();

    // Show next slide
    var nextSlide = slides[slide_index];
    nextSlide.style.display = 'block';
    nextSlide.classList.remove('animated', 'bounceInLeft', 'bounceOutLeft', 'bounceOutRight', 'bounceInRight');
    nextSlide.classList.add('animated', 'bounceInLeft');

  }

  function get_view_href() {
    // Gets the href/url to view the object once it is created
    company_id_paramater = document.location.href.split('?')[1];

    if(company_disabled_datetimes_input.getAttribute('value') === 'true') {
      view_href = document.location.origin + "/property/company-disabled-datetimes?" + company_id_paramater;
    } else {
      view_href = document.location.origin + "/property/company-disabled-days?" + company_id_paramater;
    }
    
  }

  function block_datetime_option_selected() {
    // Shows the appropriate slide when a block datetime option is clicked

    // Hide current slide
    var currentSlide = slides[slide_index];
    currentSlide.classList.remove('animated', 'bounceInRight');
    currentSlide.classList.add('animated', 'bounceOutLeft');
    currentSlide.style.display = 'none';

    // Get id of option selected to know which slide to show
    var option_id = this.getAttribute('id');
    if(option_id === 'block_datetime_option') {
      slide_index = 3;
      toggle_next_button_text();
      company_disabled_datetimes_input.setAttribute('value', 'true');
      company_disabled_days_input.setAttribute('value', 'false');
      get_view_href();
    } else if (option_id === 'block_day_option') {
      slide_index = 1;
      company_disabled_datetimes_input.setAttribute('value', 'false');
      company_disabled_days_input.setAttribute('value', 'true');
      get_view_href();
    }

    // Show next slide
    var nextSlide = slides[slide_index];
    nextSlide.style.display = 'block';
    nextSlide.classList.remove('animated', 'bounceInLeft', 'bounceOutLeft', 'bounceOutRight', 'bounceInRight');
    nextSlide.classList.add('animated', 'bounceInRight');

    // Show the slider_action_buttons_container
    slider_action_buttons_container.style.display = 'block';
    console.log(slide_index);

  }

  // Get elements needed for slider to work and cache the DOM
  var view_href = null;
  var alert_message_element = document.getElementById('alert_message');
  var next_button = document.getElementById('id_next_button');
  var back_button = document.getElementById('id_back_button');
  var slides = document.getElementsByClassName('form-slider-slide-container');
  var slides_length = slides.length;
  var slide_index = 0;
  var slider_action_buttons_container = document.getElementById('slider_action_buttons_container');
  var block_datetime_options = document.getElementsByClassName('select_block_datetime_option');
  var select_all_options_checkboxes = document.getElementsByClassName('select_all_options_checkbox');
  var company_disabled_days_input = document.getElementsByName('company_disabled_days')[0];
  var company_disabled_datetimes_input = document.getElementsByName('company_disabled_datetime')[0];
  var ul_parents_of_checkboxes = document.getElementsByClassName('option_checkboxes');

  next_button.addEventListener('click', next_button_clicked);
  back_button.addEventListener('click',  back_button_clicked);

  var l = block_datetime_options.length;
  for (var i = 0; i < l; i++) {
    block_datetime_options[i].addEventListener('click', block_datetime_option_selected);
  }

  // Checkbox events
  l = select_all_options_checkboxes.length;
  for (var j = 0; j < l; j++) {
    select_all_options_checkboxes[j].addEventListener('click', select_all);
  }

  $('#id_disabled_datetime_from').datetimepicker({
    format: 'MM/DD/YYYY hh:mm A',
    extraFormats: ['YYYY-MM-DD hh:mm:ss A'],
    sideBySide: true,
    inline: true,
    focusOnShow: false,
    showClose: true,
    ignoreReadonly: true,
    allowInputToggle: true,
  });

  $('#id_disabled_datetime_to').datetimepicker({
    format: 'MM/DD/YYYY hh:mm A',
    extraFormats: ['YYYY-MM-DD hh:mm:ss A'],
    sideBySide: true,
    inline: true,
    focusOnShow: false,
    showClose: true,
    ignoreReadonly: true,
    allowInputToggle: true,
  });

});
