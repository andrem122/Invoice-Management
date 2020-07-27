window.addEventListener('DOMContentLoaded', function() {

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

  function hideElementsOnLoad(hide_buttons) {
    // Hides all slides and makes on the first slide visible
    // Also optionally hides the slider buttons

    // Make only the first slide visible and hide the rest
    for (var i = 0; i < slides_length; i++) {
      slides[i].style.display = 'none';
    }

    // Show first slide
    slides[0].style.display = 'block';

    // Hide the buttons if needed
    if(hide_buttons === true) {
      next_button.style.display = 'none';
      back_button.style.display = 'none';
    }
  }

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

  function next_button_clicked(event, form_selector) {
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
      var form = get_parent(next_button, form_selector);
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

  // Get elements needed for slider to work
  var next_button = document.getElementById('id_next_button');
  var back_button = document.getElementById('id_back_button');
  var slides = document.getElementsByClassName('form-slider-slide-container');
  var slides_length = slides.length;
  var slide_index = 0;

  // Slider events
  var pathname = document.location.pathname;
  var form_selector = null;

  // Add company page/view
  if (pathname === '/property/add-company') {
    form_selector = '#add-company-form';
    hideElementsOnLoad(false);
  }

  next_button.addEventListener('click',  function(event) {
    next_button_clicked(event, form_selector);
  });

  back_button.addEventListener('click',  back_button_clicked);
});
