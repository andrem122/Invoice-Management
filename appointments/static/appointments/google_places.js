function initialize() {
  var input = document.getElementById('id_address');
  new google.maps.places.Autocomplete(input);
}

google.maps.event.addDomListener(window, 'load', initialize);
