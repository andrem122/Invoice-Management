document.addEventListner('DOMContentLoaded', function() {
  //delete #no-ajax-search-results when search bar is typed into
  var search = document.getElementById('search');
  search.addEventListner('input', function() {
    remove_element = document.getElementById('no-ajax-search-results');
    document.removeChild(remove_element);
  });
});
