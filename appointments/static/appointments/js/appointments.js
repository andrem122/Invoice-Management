var format = "MM/DD/YYYY hh:mm A";
var appointments = JSON.parse(document.getElementById('appointments_time').textContent);
var days_of_the_week_enabled = JSON.parse(document.getElementById('days_of_the_week_enabled').textContent);
var enabled_hours = JSON.parse(document.getElementById('hours_of_the_day_enabled').textContent);

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

function create_moments(appointments) {

  var appointmentsLength = appointments.length;
  var moments_array = [];
  for (var i = 0; i < appointmentsLength; i++) {

    time_slot = [];
    for (var j = 0; j < 2; j++) {
      var this_moment = moment(appointments[i][j], format);
      time_slot.push(this_moment);

    }

    moments_array.push(time_slot);

  }

  return moments_array;
}

$(function() {

    // Set options for appointment time field
    $('#id_time').datetimepicker({
      format: 'MM/DD/YYYY hh:mm A',
      extraFormats: ['YYYY-MM-DD hh:mm:ss A'],
      sideBySide: true,
      inline: true,
      enabledHours: enabled_hours.map(Number),
      daysOfWeekDisabled: get_days_of_the_week_disabled(days_of_the_week_enabled),
      stepping: 30,
      disabledTimeIntervals: create_moments(appointments),
      focusOnShow: false,
      showClose: true,
      ignoreReadonly: true,
      allowInputToggle: true,
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

    // Google Autocomplete
    initialize('id_address');

});
