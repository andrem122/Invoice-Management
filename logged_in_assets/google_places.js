function initialize(element_id) {
  var input = document.getElementById(element_id);
  var options = {
    types: ['address'],
    componentRestrictions: {
      country: 'us'
    }
  };
  var autocomplete = new google.maps.places.Autocomplete(input, options);
  autocomplete.setFields(['address_component']);
  return autocomplete;
}

google.maps.event.addDomListener(window, 'load', initialize);
