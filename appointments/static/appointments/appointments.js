var format = "MM/DD/YYYY hh:mm A";
var appointments = JSON.parse(document.getElementById('appointments_time').textContent);
var page_url = new URL(document.location.href);
var apartmentComplexName = page_url.searchParams.get('apartment-complex-name').toLowerCase();

if (apartmentComplexName === 'hidden villas') {
  var enabledHours = [9, 10, 11, 12, 13, 14, 15, 16, 17];
  var daysOfWeekDisabled = [0];
}

else if (apartmentComplexName === 'mayfair at lawnwood') {
  var enabledHours = [12, 13, 14, 15];
  var daysOfWeekDisabled = [0, 1, 3, 4, 5];
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
    $('#id_time').datetimepicker({
      format: 'MM/DD/YYYY hh:mm A',
      extraFormats: ['YYYY-MM-DD hh:mm:ss A'],
      sideBySide: true,
      inline: true,
      enabledHours: enabledHours,
      daysOfWeekDisabled: daysOfWeekDisabled,
      stepping: 30,
      disabledTimeIntervals: create_moments(appointments),
      focusOnShow: false,
      showClose: true,
      ignoreReadonly: true,
      allowInputToggle: true,
    });
});
