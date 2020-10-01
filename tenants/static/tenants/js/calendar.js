window.addEventListener('DOMContentLoaded', function() {
  console.log('DOM content loaded');

  $('#id_lease_begin').datetimepicker({
    format: 'MM/DD/YYYY',
    extraFormats: ['YYYY-MM-DD'],
    sideBySide: true,
    inline: true,
    focusOnShow: false,
    showClose: true,
    ignoreReadonly: true,
    allowInputToggle: true,
  });
});
