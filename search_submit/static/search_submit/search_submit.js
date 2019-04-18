function delete_no_ajax_search_results() {
  var element_to_remove = document.getElementsByClassName('no-ajax-search-results')[0];

  if (typeof element_to_remove !== 'undefined') {

    var parent = element_to_remove.parentElement;
    parent.removeChild(element_to_remove);

  }

}

document.addEventListener('DOMContentLoaded', function() {

  var search = document.getElementById('search');
  search.addEventListener('input', delete_no_ajax_search_results);

});
