document.addEventListener('DOMContentLoaded', function() {
  //delete #no-ajax-search-results when search bar is typed into
  var search = document.getElementById('search');
  search.addEventListener('input', function() {
    var remove_elements = document.getElementsByClassName('no-ajax-search-results');
    l = remove_elements.length;
    for (var i = 0; i < l; i++) {
      var parent = remove_elements[i].parentElement;
      parent.removeChild(remove_elements[i]);
    }
  });
});
