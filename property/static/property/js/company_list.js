window.addEventListener('DOMContentLoaded', navigate_to_appointment())

function navigate_to_appointment() {
  // Navigates to the create appointment screen for the company selected
  // When the div is clicked on, navigate to the appointment screen
  var rows = document.getElementsByClassName('table-row');
  console.log(rows);

  length = rows.length;
  for(var i = 0; i < length; i++) {
    // Add event listener to each element in the array
    rows[i].addEventListener('click', function() {
      console.log('Table row clicked!');
      // Get the data-appointment-link attribute value
      var appointment_link = this.getAttribute('data-appointment-link');
      window.location = appointment_link;
    });
  }
}
