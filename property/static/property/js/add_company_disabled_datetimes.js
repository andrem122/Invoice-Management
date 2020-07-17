window.addEventListener('DOMContentLoaded', function() {

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
