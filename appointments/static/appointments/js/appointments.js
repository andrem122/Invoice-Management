$(function() {
  // Google Autocomplete
  var autocomplete = initialize('id_address');

  // Google places events
  google.maps.event.addListener(autocomplete, 'place_changed', fill_in_address);
  var format = "MM/DD/YYYY hh:mm A";
  var appointments = JSON.parse(document.getElementById('appointments_time').textContent);
  var disabled_datetimes = JSON.parse(document.getElementById('disabled_datetimes').textContent);
  var days_of_the_week_enabled = JSON.parse(document.getElementById('days_of_the_week_enabled').textContent);
  var enabled_hours = JSON.parse(document.getElementById('hours_of_the_day_enabled').textContent);
  var allow_same_day_appointments = JSON.parse(document.getElementById('allow_same_day_appointments').textContent);
  var city_input = document.getElementById('id_city');
  var zip_input = document.getElementById('id_zip');

  // Set the minimum date for the calendar
  var minDate = new Date();
  if(allow_same_day_appointments === false) {
    minDate.setHours(minDate.getHours() + 24);
  }

  function create_moments(datetimes) {

    var datetimesLength = datetimes.length;
    var moments_array = [];
    for (var i = 0; i < datetimesLength; i++) {

      time_slot = [];
      for (var j = 0; j < 2; j++) {
        var this_moment = moment(datetimes[i][j], format);
        time_slot.push(this_moment);

      }

      moments_array.push(time_slot);

    }

    return moments_array;
  }


  function get_days_of_the_week_disabled(days_of_the_week_enabled) {
    // Gets the days of the week that are disabled from the enabled days array

    days_of_the_week_enabled = days_of_the_week_enabled.map(Number);
    days_of_the_week_disabled = [];
    for(var i = 0; i < 7; i++) {
      // If loop variable IS in the days_of_the_week_enabled array, then do NOT include it in the new array
      if(!days_of_the_week_enabled.includes(i)) {
        days_of_the_week_disabled.push(i);
      }

    }

    return days_of_the_week_disabled;
  }

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

      // else if(addressType == 'administrative_area_level_1') { // State
      //   state = place.address_components[i].short_name;
      // }

      else if(addressType == 'postal_code') { // Zip code
        zip = place.address_components[i].long_name;
      }

    }

    // Set the values for the input fields
    city_input.value = city;
    // state_input.value = state;
    zip_input.value = zip;
  }


  var all_disabled_times = disabled_datetimes.concat(appointments);
  // Set options for appointment time field
  $('#id_time').datetimepicker({
    format: 'MM/DD/YYYY hh:mm A',
    extraFormats: ['YYYY-MM-DD hh:mm:ss A'],
    sideBySide: true,
    inline: true,
    enabledHours: enabled_hours.map(Number),
    daysOfWeekDisabled: get_days_of_the_week_disabled(days_of_the_week_enabled),
    stepping: 30,
    disabledTimeIntervals: create_moments(all_disabled_times),
    focusOnShow: false,
    showClose: true,
    ignoreReadonly: true,
    allowInputToggle: true,
    minDate: minDate,
  });

  // Set options for date of birth field if it exists
  var DOBExists = document.getElementById('id_date_of_birth');
  if (DOBExists !== null) {
    $('#id_date_of_birth').datetimepicker({
      format: 'MM/DD/YYYY',
      extraFormats: ['YYYY-MM-DD'],
      sideBySide: true,
      inline: true,
      focusOnShow: false,
      showClose: true,
      ignoreReadonly: true,
      allowInputToggle: true,
      defaultDate: new Date(1975, 0, 1, 00, 01),
      viewMode: 'years',
    });
  }
});
